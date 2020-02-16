#!/usr/bin/python3
#
#   A. Gnias
#
#   test_send_email.py - Tests sending a generic email; replace None in variables to run
#
#   Linux 4.18.0-18-generic #19-Ubuntu
#   Python 3.7.5
#   Vim 8.0

import sys

sys.path.append("../")
import secret_santa


from_address = None
from_password = None
gifter_email = from_address

subject = "Secret Santa Assignment"
body = "This is a test message"
message = "Subject: {}\n\n{}".format(subject, body)

secret_santa.send_email(from_address, from_password, gifter_email, message)
