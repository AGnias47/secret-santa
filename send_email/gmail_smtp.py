#!/usr/bin/python3
#
#   A. Gnias
#
#   Linux 4.18.0-18-generic #19-Ubuntu
#   Python 3.7.5
#   Vim 8.0


import smtplib


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
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, smtp_message)
        server.close()
        print("Email sent!")
    except Exception as e:
        print("Error sending email to {}".format(recipient))
        print(e)
        return False
    return True
