#!/usr/bin/python3

from send_email.gmail_smtp import GmailSMTPSender
from send_email.aws_ses import AwsSesSender
from send_email.gmail_api import GmailApiSender

import pytest

SMTP = False
SES = False
API = True


def test_smtp():
    if SMTP:
        sender = GmailSMTPSender(None, None)
        assert sender.send_email(
            recipient="", subject="Secret Santa Assignment", body="This is a test message from Gmail SMTP"
        )


def test_ses():
    if SES:
        sender = AwsSesSender(None)
        assert sender.send_email(
            recipient="", subject="Secret Santa Assignment", body="This is a test message from Gmail SMTP"
        )


def test_gmail_api():
    if API:
        sender = GmailApiSender(None)
        assert sender.send_email(
            recipient="", subject="Secret Santa Assignment", body="This is a test message from Gmail SMTP"
        )


if __name__ == "__main__":
    pytest.main()
