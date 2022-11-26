#!/usr/bin/python3

"""
Module for sending emails via the Gmail API
"""

import base64
from email.mime.text import MIMEText
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


class GmailApiSender:
    def __init__(
        self,
        sender_email,
        cred_path,
        token_path,
    ):
        """
        Initialize class and authenticate with the Gmail API. Requires pre-existing credentials file and enablement of
        the Gmail API

        Parameters
        ----------
        sender_email: str
        cred_path: str
            Path to credentials.json. Create OAuth2 credentials in Google Developer Console and then download
        token_path: str
            Path to token.json with refresh token. Does not need to exist
        """
        self.sender_email = sender_email
        creds = None
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
                creds = flow.run_local_server(port=52381)
            # Save the credentials for the next run
            with open(token_path, "w") as token:
                token.write(creds.to_json())
        self.service = build("gmail", "v1", credentials=creds)

    def send_email(self, recipient, subject, body):
        """
        Sends an email through a Gmail account using the Gmail API

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
        message = MIMEText(body)
        message["to"] = recipient
        message["From"] = self.sender_email
        message["subject"] = subject
        mime_message = {"raw": base64.urlsafe_b64encode(message.as_string().encode()).decode()}
        try:
            self.service.users().messages().send(userId="me", body=mime_message).execute()
        except Exception as e:
            print(f"Error sending email to {recipient}")
            print(e)
            return False
        return True
