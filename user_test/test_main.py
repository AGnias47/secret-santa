#!/usr/bin/python3
#
#    Andy Gnias
#
#    test_main.py - Tests script functionality without sending emails
#
#    Kubuntu 5.16.5
#    Python 3.7.5
#

import sys

sys.path.append(".")
from secret_santa.Participant import create_participant_list
from secret_santa.selections import make_selections
from secret_santa.email import Email


def mock_send_email(*args, **kwargs):
    pass


if __name__ == "__main__":
    participants = create_participant_list("user_test/names.csv", "user_test/exceptions.csv")
    check_success = make_selections(participants)  # The Algorithm
    if not check_success:
        sys.exit("Secret Santa selections were unable to be made with the inputs provided")
    emailer = Email(None, None, mock_send_email)
    emailer.email_participants(participants)
