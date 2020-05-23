#!/usr/bin/python3
#
#    Andy Gnias
#
#    secret_santa.py - Informs Secret Santa participants of their Secret Santa
#    via email, making it blind from the person running the code.
#
#    Kubuntu 5.16.5
#    Python 3.7.5
#

import argparse
import sys
from random import shuffle
from getpass import getpass
import pathlib
import re as regex

import send_emails


class MissingRequiredArgument(Exception):
    """
    Raise this exception if a required argument is not provided
    """

    def __init__(self, msg=None):
        super().__init__(msg)


class FlagConflict(Exception):
    """
    Raise this exception if conflicting flags are provided
    """

    def __init__(self, msg=None):
        super().__init__(msg)


def process_commandline_parameters():
    """
    Processes commandline parameters for dynamic use of email, password, csv files, and exchange date.
    Not adaptable to other scripts in its hard-coded form.  

    Returns
    -------
    tuple: (str / tuple, str, str, str, function)  
        email or (email, password), names csv, exceptions csv, exchange date, and function for sending emails

    """
    parser = argparse.ArgumentParser()
    # Want the user to explicitly set the email protocol; currently Gmail and Amazon SES supported
    parser.add_argument("--gmail", action="store_true", help="Use Gmail SMTP to send emails")
    parser.add_argument("--ses", action="store_true", help="Use Amazon SES to send emails")
    parser.add_argument("-e", "--email", help="Sender's Email address")
    parser.add_argument("-p", "--password", help="Sender's Email password; only necessary for SMTP through Gmail")
    parser.add_argument("-n", "--names", help="CSV containing participants names and email addresses")
    parser.add_argument(
        "-x", "--exceptions", help="CSV containing participant's name followed by people they should not be paired with"
    )
    parser.add_argument("-d", "--date", help="Date of the Secret Santa exchange")
    args = parser.parse_args()
    if not args.gmail and not args.ses:
        raise MissingRequiredArgument(
            "Email Protocol must be explicitly set, either --gmail or --ses. See README for further details"
        )
    if args.gmail and args.ses:
        raise FlagConflict("Only one of --gmail or --ses can be provided")
    if args.email:
        email = args.email
    else:
        email = input("Sender's email: ").strip()
    if args.gmail:
        send_email_func = send_emails.send_gmail_smtp_email
        print("Using Gmail SMTP instead of Amazon SES to send emails")
        if args.password:
            password = args.password
        else:
            password = getpass("Password for sender's email: ").strip()
        email = (email, password)
    if args.ses:
        print("Using Amazon SES to send emails")
        send_email_func = send_emails.send_amazon_ses_email
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
    return email, names_filename, exceptions_filename, exchange_date_string, send_email_func


def generate_names_dictionary(fname):
    """
    Generates a dict of the form d[name] = email from a csv file.

    Parameters
    ----------
    fname: str  
        File path to CSV of the form [name, email address] in the cwd  

    Returns
    -------
    dict  
        key: name, value: email  

    """
    d = dict()
    with open(fname, "r") as f:
        for line in f:
            contents = line.strip().split(",")
            name = contents[0].strip()
            email = contents[1].strip()
            d[name] = email
    f.close()
    return d


def generate_exceptions_dict(fname):
    """
    Generates a dictionary where each entry is a dict of the form:  
        d[Name] = List of names they can't be matched with

    Parameters
    ----------
    fname: str  
        File path to CSV of the form [name, person to exclude_1, ..., person to exclude_n] in the cwd  

    Returns
    -------
    dict:  
        Key: Name, Value: List of names to exclude  

    """
    if fname is None:
        return None
    d = dict()
    with open(fname, "r") as f:
        for line in f:
            contents = line.strip().split(",")
            names_to_exclude = list()
            for i, ex in enumerate(contents):
                if i == 0:
                    name = ex.strip()
                else:
                    names_to_exclude.append(ex.strip())
            d[name] = names_to_exclude
    f.close()
    return d


def make_selections(names, exceptions, upper_limit=10000):
    """
    Makes the Secret Santa selections

    Parameters
    ----------
    names: list  
        Names of participants  
    exceptions: dict  
        Key: Name, Value: List of names to exclude  
    upper_limit: int (default is 10000)  
        Max sorting attempts to execute  

    Returns
    -------
    bool  
        True if list was properly sorted, else False. Names list is mutated in new shuffled order  

    """
    list_sorted = False
    counter = 0
    while not list_sorted and counter < upper_limit:  # shuffle list until it abides by conditions set
        counter += 1
        shuffle(names)
        list_sorted = check_conditions(names, exceptions)
    return list_sorted


def check_conditions(names_list, exceptions_dict):
    """
    Check to prevent people who shouldn't get each other from getting each other, ex. couples

    Parameters
    ----------
    names_list: list  
        Names of participants  
    exceptions_dict: dict
        Key: Name, Value: List of names to exclude  

    Returns
    -------
    bool  
        True if no exceptions are violated, else False  

    """
    for i, name in enumerate(names_list):
        if names_list[i - 1] in exceptions_dict.get(name, []):
            return False
    return True


def compose_message_body(gifter, recipient, exchange_date=None):
    """
    Generates the content of the Secret Santa email.

    Parameters
    ----------
    gifter: str  
        Name of gifter  
    recipient: str  
        Name of gift recipient  
    exchange_date: str (default is None)  
        If provided, specifies the exchange date in the message  

    Returns
    -------
    str  
        Message compatible with SMTP email  

    """
    assignment = "{}, \n\nYou have been assigned to be {}'s Secret Santa!".format(gifter, recipient)
    exchange = ""
    if exchange_date is not None:
        exchange = " Please purchase a gift for them before the gift exchange on {}.".format(exchange_date)
    return assignment + exchange


def email_participants(names_list, names_dict, email, send_email, exchange_date=None, test=False):
    """
    Informs participants who they have for Secret Santa via email  

    Parameters
    ----------
    names_list: list  
        list of participant names  
    names_dict: dict  
        Key: Name, Value: Email address of Name  
    email: str / tuple  
        Email address / tuple of (email address, password) to send emails from  
    send_email: function  
        Function from send_emails module used for sending emails (currently Gmail SMTP or Amazon SES)  
    exchange_date: str (default is None)  
        Date of the gift exchange; can be None if exchange date is undecided  
    test: bool (default is False)  
        If True, do not send an actual email and only print to stdout, else actually send an email  

    Returns
    -------
    list  
        List of return values (True or False) from sending emails to participants  

    """
    subject = "Secret Santa Assignment"
    sent_emails_boolean_list = list()
    # first person gifts to last name in 'names list
    gifter = names_list[0]
    gifter_email = names_dict[gifter]
    recipient = names_list[len(names_list) - 1]
    # compose a message based on the selected gifter and recipient
    message_body = compose_message_body(gifter, recipient, exchange_date)
    if test:
        print(message_body, sep="\n\n")
    else:
        status = send_email(email, gifter_email, subject, message_body)
        sent_emails_boolean_list.append(status)
    # everyone else gifts to the person above them in names_list
    for i, name in enumerate(names_list):
        if i == (len(names_list) - 1):  # All gifts processed; prevents out of range error
            continue
        gifter = names_list[i + 1]
        gifter_email = names_dict[gifter]
        recipient = names_list[i]
        message_body = compose_message_body(gifter, recipient, exchange_date)
        if test:
            print(message_body, sep="\n\n")
        else:
            status = send_email(email, gifter_email, subject, message_body)
            sent_emails_boolean_list.append(status)
    return sent_emails_boolean_list


if __name__ == "__main__":
    # Get command line parameters
    try:
        (
            sender_email,
            names_fname,
            exceptions_fname,
            exchange_date,
            send_email_function,
        ) = process_commandline_parameters()
    except (MissingRequiredArgument, FlagConflict) as err:
        sys.exit(err)
    # Read values from files provided
    try:
        names_dictionary = generate_names_dictionary(names_fname)
    except FileNotFoundError:
        sys.exit(f"Names list file {names_fname} could not be found. Exiting.")
    try:
        exceptions_dictionary = generate_exceptions_dict(exceptions_fname)
    except FileNotFoundError:
        sys.exit(f"Exceptions list file {exceptions_fname} could not be found. Exiting.")
    # Determine Secret Santa assignments
    participant_names_list = list(names_dictionary.keys())
    check_success = make_selections(participant_names_list, exceptions_dictionary)  # The Algorithm
    if not check_success:
        sys.exit("Secret Santa selections were unable to be made with the inputs provided")
    # Send emails informing participants of their assignment
    email_status = email_participants(
        participant_names_list, names_dictionary, sender_email, send_email_function, exchange_date
    )
    if all(email_status):
        print("All emails sent successfully")
    else:
        print("There was an error sending one or more emails")
