#!/usr/bin/python3

import smtplib

class GmailSMTP:
    def __init__(self, sender_email, sender_password, port=465, smtp_server="smtp.gmail.com"):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.port = port


def send_email(recipient, subject, body):
    """
    Sends an email through a Gmail account using the SMTP protocol

    Parameters
    ----------
    recipient: str
        Email address to send to
    subject: str
        Subject of the email
    body: str
        Body of the email

    Returns
    -------
    bool
        True upon successful completion, else False

    Notes
    -------
    Successful execution of the function does not necessarily mean that an email was sent

    """
    smtp_message = "Subject: {}\n\n{}".format(subject, body)
    try:
        server = smtplib.SMTP_SSL(self.smtp_server, self.port)
        server.ehlo()
        server.login(self.sender_email, self.sender_password)
        server.sendmail(self.sender_email, recipient, smtp_message)
        server.close()
        print("Email sent!")
    except Exception as e:
        print("Error sending email to {}".format(recipient))
        print(e)
        return False
    return True

