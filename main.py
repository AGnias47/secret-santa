#!/usr/bin/env python

import argparse
from getpass import getpass
from os import getenv
import pathlib
import re as regex

from secret_santa.Participant import create_participant_hash
from secret_santa.selections import make_selections
from secret_santa.email import invite_participants, email_participants
from send_email.gmail_api import GmailApiSender
from send_email.aws_ses import AwsSesSender
from send_email.gmail_smtp import GmailSMTPSender


"""
Informs Secret Santa participants of their Secret Santa via email
"""


def process_commandline_parameters():
    """
    Processes commandline parameters for dynamic use of email, password, csv files, and exchange date.
    Not adaptable to other scripts in its hard-coded form.

    Returns
    -------
    tuple: (Object, str, str, str, function)
        Class object for sending emails, names csv, exceptions csv, exchange date, and function for sending emails

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--email", help="Sender's Email address")
    parser.add_argument(
        "-p",
        "--password",
        help="Sender's Email password; only necessary for SMTP through Gmail",
    )
    parser.add_argument(
        "-m",
        "--method",
        help="Method for sending emails; One of gmailapi (default), ses, or smtp.",
    )
    parser.add_argument(
        "-n", "--names", help="CSV containing participants names and email addresses"
    )
    parser.add_argument(
        "-x",
        "--exceptions",
        help="CSV containing participant's name followed by people they should not be paired with",
    )
    parser.add_argument("-d", "--date", help="Date of the Secret Santa exchange")
    parser.add_argument(
        "-i",
        "--invitation",
        help="Sends an invitation email instead of pairing participants for the exchange",
        action="store_true",
    )
    args = parser.parse_args()
    if args.email:
        email = args.email
    else:
        email = input("Sender's email: ").strip()
    if args.method:
        if args.method.casefold() == "gmailapi".casefold():
            cred_path, token_path = get_gmail_api_env_vars()
            sender_object = GmailApiSender(email, cred_path, token_path)
        elif args.method.casefold() == "ses".casefold():
            sender_object = AwsSesSender(email)
        elif args.method.casefold() == "smtp".casefold():
            if args.password:
                password = args.password
            else:
                password = getpass("Password for sender's email: ").strip()
            sender_object = GmailSMTPSender(email, password)
        else:
            raise ValueError(
                "Invalid send method specified; must be one of gmailapi, ses, or smtp"
            )
    else:
        cred_path, token_path = get_gmail_api_env_vars()
        sender_object = GmailApiSender(email, cred_path, token_path)
    if args.names:
        names_filename = args.names
    else:
        generic_names_file = pathlib.Path("pii/names.csv")
        if generic_names_file.is_file():
            print("Using pii/names.csv from cwd")
            names_filename = "pii/names.csv"
        else:
            names_filename = input("File containing names,emails: ").strip()
    if args.exceptions:
        exceptions_filename = args.exceptions
    else:
        generic_exceptions_file = pathlib.Path("pii/exceptions.csv")
        if generic_exceptions_file.is_file():
            print("Using pii/exceptions.csv from cwd")
            exceptions_filename = "pii/exceptions.csv"
        else:
            confirm_exceptions_file = input(
                "No exceptions file provided (-x). Would you like to use one? "
            ).strip()
            if regex.match("[Yy]", confirm_exceptions_file):
                exceptions_filename = input("File name: ").strip()
            else:
                exceptions_filename = None
    if args.date:
        exchange_date_string = args.date
    elif not args.invitation:
        confirm_exchange_date = input(
            "Would you like to specify an exchange date?"
        ).strip()
        if regex.match("[Yy]", confirm_exchange_date):
            exchange_date_string = input(
                "Specify date however you would like integration_test displayed: "
            ).strip()
        else:
            exchange_date_string = None
    else:
        exchange_date_string = None
    return (
        sender_object,
        names_filename,
        exceptions_filename,
        exchange_date_string,
        args.invitation,
    )


def get_gmail_api_env_vars():
    """
    Checks for necessary environment variables for the Gmail API, and raises an error if not present

    Returns
    -------
    str, str
        Path to Google Project credentials, path to save token
    """
    errors = None
    if not (cred_path := getenv("CRED_PATH")):
        errors = "CRED_PATH variable is not set"
    if not (token_path := getenv("TOKEN_PATH")):
        if errors:
            errors = "CRED_PATH and TOKEN_PATH variables are not set"
        else:
            errors = "TOKEN_PATH variable is not set"
    if errors:
        raise RuntimeError(errors)
    return cred_path, token_path


if __name__ == "__main__":
    (
        sender,
        names_fname,
        exceptions_fname,
        exchange_date,
        invitation,
    ) = process_commandline_parameters()
    participants = create_participant_hash(names_fname, exceptions_fname)
    if invitation:
        email_status = invite_participants(sender, participants)
    else:
        order = make_selections(participants)  # The Algorithm
        email_status = email_participants(sender, participants, order, exchange_date)
    if all(email_status):
        print("All emails sent successfully")
    else:
        print("There was an error sending one or more emails")
