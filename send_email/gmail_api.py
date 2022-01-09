#!/usr/bin/python3

import smtplib

# Resource: https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python

class GmailApiSender:
    def __init__(self):
        pass


def send_email(sender, recipient, subject, body):
    """
    Sends an email through a Gmail account using the SMTP protocol

    Parameters
    ----------
    sender: tuple
        Email address to send from, Password for email address
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
    sender_email = sender[0]
    sender_password = sender[1]
    smtp_message = "Subject: {}\n\n{}".format(subject, body)
    message = MIMEText(body)
    message['to'] = recipient
    message['from'] = sender_email
    message['subject'] = subject
    mime_message = {'raw': base64.urlsafe_b64encode(message.as_string())}
    try:
        message = (service.users().messages().send(userId=sender_email, body=mime_message).execute())
    print(f"Message Id: {message['id']}")
    except errors.HttpError, error:
        print(error)
    return True
