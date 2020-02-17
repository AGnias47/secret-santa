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

import sys
import smtplib
from random import shuffle
import getopt
from getpass import getpass
import pathlib
import re as regex


def process_commandline_parameters():
    """
    Processes commandline parameters for dynamic use of email, password, csv files, and exchange date.
    Not adaptable to other scripts in its hard-coded form.

    Returns
    -------
    tuple: (str, str, str, str, str)  
        email, password, and names csv, exceptions csv, and exchange date  

    """
    options, arguments = getopt.getopt(
        sys.argv[1:], "e:p:n:x:d:", ["email=", "password=", "names=", "exceptions=", "date="]
    )
    for o, a in options:
        if o in ("-e", "--email"):
            email = a
        elif o in ("-p", "--password"):
            password = a
        elif o in ("-n", "--names"):
            names_fname = a
        elif o in ("-x", "--exceptions"):
            exceptions_fname = a
        elif o in ("-d", "--date"):
            exchange_date = a
        else:
            print("Unhandled option; ignoring {1}", o)
    try:
        email
    except NameError:
        email = input("Sender's email: ").strip()
    try:
        password
    except NameError:
        password = getpass("Password for sender's email: ").strip()
    try:
        names_fname
    except NameError:
        generic_names_file = pathlib.Path("names.csv")
        if generic_names_file.is_file():
            print("Using names.csv from cwd")
            names_fname = "names.csv"
        else:
            names_fname = input("File containing names,emails: ").strip()
    try:
        exceptions_fname
    except NameError:
        generic_exceptions_file = pathlib.Path("exceptions.csv")
        if generic_exceptions_file.is_file():
            print("Using exceptions.csv from cwd")
            exceptions_fname = "exceptions.csv"
        else:
            confirm_exceptions_file = input("No exceptions file provided (-x). Would you like to use one? ").strip()
            if regex.match("[Yy]", confirm_exceptions_file):
                exceptions_fname = input("File name: ").strip()
            else:
                exceptions_fname = None
    try:
        exchange_date
    except NameError:
        confirm_exchange_date = input("Would you like to specify an exchange date?").strip()
        if regex.match("[Yy]", confirm_exchange_date):
            exchange_date = input("Specify date however you would like it displayed: ").strip()
        else:
            exchange_date = None
    return email, password, names_fname, exceptions_fname, exchange_date


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


def Make_Selections(names, exceptions, upper_limit=10000):
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


def check_conditions(names_list, exceptionsDict):
    """
    Check to prevent people who shouldn't get each other from getting each other, ex. couples

    Parameters
    ----------
    names_list: list  
        Names of participants  
    exceptionsDict: dict  
        Key: Name, Value: List of names to exclude  

    Returns
    -------
    bool  
        True if no exceptions are violated, else False  

    """
    for i, name in enumerate(names_list):
        if names_list[i - 1] in exceptionsDict.get(name, []):
            return False
    return True


def compose_message(gifter, recipient, exchange_date=None):
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
    subject = "Secret Santa Assignment"
    assignment = "{}, \n\nYou have been assigned to be {}'s Secret Santa!".format(gifter, recipient)
    exchange = ""
    if exchange_date is not None:
        exchange = " Please purchase a gift for them before the gift exchange on {}.".format(exchange_date)
    body = assignment + exchange
    message = "Subject: {}\n\n{}".format(subject, body)
    return message


def send_email(from_address, from_password, gifter_email, smtp_message):
    """
    Sends Secret Santa email

    Parameters
    ----------
    from_address: str  
        Email address to send from  
    from_password: str  
        Password for from_address email  
    gifter_email: str  
        Email address to send to  
    smtp_message: str  
        Message to email  

    Returns
    -------
    bool  
        True upon successful completion, else False  

    Notes
    -------
    Successful execution of the function does not necessarily mean that an email was sent  

    """
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(from_address, from_password)
        server.sendmail(from_address, gifter_email, smtp_message)
        server.close()
        print("Email sent!")
    except Exception as e:
        print("Error sending email to {}".format(gifter_email))
        print(e)
        return False
    return True


def email_participants(names_list, names_dict, email, password, exchange_date=None, test=False):
    """
    Informs participants who they have for Secret Santa via email  

    Parameters
    ----------
    names_list: list  
        list of participant names  
    names_dict: dict  
        Key: Name, Value: Email address of Name  
    email: str  
        Email address to send from  
    password: str  
        Password of email address  
    exchange_date: str (default is None)  
        Date of the gift exchange; can be None if exchange date is undecided  
    test: bool (default is False)  
        If True, do not send an actual email and only print to stdout, else actually send an email  

    Returns
    -------
    bool  
        True upon completion  

    """
    # first person gifts to last name in 'names list
    gifter = names_list[0]
    gifter_email = names_dict[gifter]
    recipient = names_list[len(names_list) - 1]
    # compose a message based on the selected gifter and recipient
    message_body = compose_message(gifter, recipient, exchange_date)
    if test:
        print(message_body, sep="\n\n")
    else:
        send_email(email, password, gifter_email, message_body)
    # everyone else gifts to the person above them in names_list
    for i, name in enumerate(names_list):
        if i == (len(names_list) - 1):  # All gifts processed; prevents out of range error
            continue
        gifter = names_list[i + 1]
        gifter_email = names_dict[gifter]
        recipient = names_list[i]
        message_body = compose_message(gifter, recipient, exchange_date)
        if test:
            print(message_body, sep="\n\n")
        else:
            send_email(email, password, gifter_email, message_body)
    return True


if __name__ == "__main__":
    try:
        email, password, names_fname, exceptions_fname, exchange_date = process_commandline_parameters()
    except getopt.GetoptError as err:
        sys.exit(err)
    names_dictionary = generate_names_dictionary(names_fname)
    exceptions_dictionary = generate_exceptions_dict(exceptions_fname)
    names_list = list(names_dictionary.keys())
    check_success = Make_Selections(names_list, exceptions_dictionary)  # The Algorithm
    if not check_success:
        sys.exit("Secret Santa selections were unable to be made with the inputs provided")
    email_participants(names_list, names_dictionary, email, password, exchange_date)
