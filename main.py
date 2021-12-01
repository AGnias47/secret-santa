#!/usr/bin/python3
#
#    Andy Gnias
#
#    main.py - Informs Secret Santa participants of their Secret Santa
#    via email, making it blind from the person running the code.
#
#    Kubuntu 5.16.5
#    Python 3.7.5
#

from secret_santa.Participant import create_participant_list
from secret_santa.selections import make_selections
from secret_santa.email import Email

import argparse
from getpass import getpass
import pathlib
import re as regex
import sys


def process_commandline_parameters():
    """
    Processes commandline parameters for dynamic use of email, password, csv files, and exchange date.
    Not adaptable to other scripts in its hard-coded form.

    Returns
    -------
    tuple: (str / tuple, str, str, str, function)
        email, password, names csv, exceptions csv, exchange date, and function for sending emails

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--email", help="Sender's Email address")
    parser.add_argument("-p", "--password", help="Sender's Email password; only necessary for SMTP through Gmail")
    parser.add_argument("-n", "--names", help="CSV containing participants names and email addresses")
    parser.add_argument(
        "-x", "--exceptions", help="CSV containing participant's name followed by people they should not be paired with"
    )
    parser.add_argument("-d", "--date", help="Date of the Secret Santa exchange")
    args = parser.parse_args()
    if args.email:
        email = args.email
    else:
        email = input("Sender's email: ").strip()

    if args.password:
        password = args.password
    else:
        password = getpass("Password for sender's email: ").strip()
    if args.names:
        names_filename = args.names
    else:
        generic_names_file = pathlib.Path("names.csv")
        if generic_names_file.is_file():
            print("Using names.csv from cwd")
            names_filename = "names.csv"
        else:
            names_filename = input("File containing names,emails: ").strip()
    if args.exceptions:
        exceptions_filename = args.exceptions
    else:
        generic_exceptions_file = pathlib.Path("exceptions.csv")
        if generic_exceptions_file.is_file():
            print("Using exceptions.csv from cwd")
            exceptions_filename = "exceptions.csv"
        else:
            confirm_exceptions_file = input("No exceptions file provided (-x). Would you like to use one? ").strip()
            if regex.match("[Yy]", confirm_exceptions_file):
                exceptions_filename = input("File name: ").strip()
            else:
                exceptions_filename = None
    if args.date:
        exchange_date_string = args.date
    else:
        confirm_exchange_date = input("Would you like to specify an exchange date?").strip()
        if regex.match("[Yy]", confirm_exchange_date):
            exchange_date_string = input("Specify date however you would like it displayed: ").strip()
        else:
            exchange_date_string = None
    return email, password, names_filename, exceptions_filename, exchange_date_string


if __name__ == "__main__":
    # Get command line parameters
    sender_email, sender_password, names_fname, exceptions_fname, exchange_date = process_commandline_parameters()
    # Read values from files provided
    participants = create_participant_list(names_fname, exceptions_fname)
    # Determine Secret Santa assignments
    check_success = make_selections(participants)  # The Algorithm
    if not check_success:
        sys.exit("Secret Santa selections were unable to be made with the inputs provided")
    # Send emails informing participants of their assignment
    emailer = Email(sender_email, sender_password)
    email_status = emailer.send_email(participants, exchange_date)
    if all(email_status):
        print("All emails sent successfully")
    else:
        print("There was an error sending one or more emails")
