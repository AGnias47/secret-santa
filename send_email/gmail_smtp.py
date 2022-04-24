#!/usr/bin/python3

"""
Module for sending emails via SMTP
"""

import smtplib


class GmailSMTPSender:
    def __init__(self, sender_email, sender_password, port=465, smtp_server="smtp.gmail.com"):
        """
        Initialize class

        Parameters
        ----------
        sender_email: str
        sender_password: str
        port: int
        smtp_server: str
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.port = port

    def send_email(self, recipient, subject, body):
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
        smtp_message = f"Subject: {subject}\n\n{body}"
        try:
            server = smtplib.SMTP_SSL(self.smtp_server, self.port)
            server.ehlo()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, recipient, smtp_message)
            server.close()
            print("Email sent!")
        except Exception as e:
            print(f"Error sending email to {recipient}")
            print(e)
            return False
        return True
