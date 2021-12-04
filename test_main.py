#!/usr/bin/python3
#
#    Andy Gnias
#
#    test_main.py - Manual sanity check for viewing how emails will be sent
#
#    Kubuntu 5.16.5
#    Python 3.7.5
#

from secret_santa.Participant import create_participant_hash
from secret_santa.selections import make_selections
from secret_santa.email import Email


def mock_send_email(email, gift_giver, subject, message_body):
    print(message_body, end="\n\n")


if __name__ == "__main__":
    participants = create_participant_hash("test/names.csv", "test/exceptions.csv")
    order = make_selections(participants)  # The Algorithm
    emailer = Email(None, None, mock_send_email)
    emailer.email_participants(participants, order, "December 25")
