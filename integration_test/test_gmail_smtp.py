#!/usr/bin/python3

from send_email.gmail_smtp import send_email

import pytest


def test_send_email():
    assert send_email(
        (None, None), recipient="", subject="Secret Santa Assignment", body="This is a test message from Gmail SMTP"
    )


if __name__ == "__main__":
    pytest.main()
