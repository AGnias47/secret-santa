#!/usr/bin/python3

"""
Module for sending emails via Amazon's Simple Email Service
"""

import boto3
from botocore.exceptions import ClientError


class AwsSesSender:
    def __init__(self, sender_email):
        """
        Initialize class

        Parameters
        ----------
        sender_email: str
        """
        self.sender_email = sender_email

    def send_email(self, recipient, subject, body):
        """
        Adapted from the sample script at:
        https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html
        Sends an email utilizing Amazon SES

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
        client = boto3.client("ses")
        try:
            client.send_email(
                Destination={
                    "ToAddresses": [
                        recipient,
                    ],
                },
                Message={
                    "Body": {
                        "Text": {"Charset": "UTF-8", "Data": body},
                    },
                    "Subject": {"Charset": "UTF-8", "Data": subject},
                },
                Source=self.sender_email,
            )
        except ClientError as e:
            print(e.response["Error"]["Message"])
            print(f"Error sending email to {recipient}")
            return False
        return True
