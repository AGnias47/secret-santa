#!/usr/bin/python3
#
#   A. Gnias
#
#   send_email_test.py - Tests sending a generic email; replace None in variables to run
#
#   Linux 4.18.0-18-generic #19-Ubuntu
#   Python 3.7.5
#   Vim 8.0

import sys

sys.path.append("../")
from send_email.gmail_smtp import send_email

from_address = None
from_password = None
gifter_email = from_address

subject = "Secret Santa Assignment"
message_gmail = "This is a test message from Gmail SMTP"
message_ses = "This is a test message from Amazon SES"
send_email((from_address, from_password), gifter_email, subject, message_gmail)
