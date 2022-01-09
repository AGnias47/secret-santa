#!/usr/bin/python3
#
#   A. Gnias
#
#   Linux 4.18.0-18-generic #19-Ubuntu
#   Python 3.7.5
#   Vim 8.0


import smtplib
import boto3
from botocore.exceptions import ClientError


def send_amazon_ses_email(sender, recipient, subject, body):
    """
    Adapted from the sample script at: 
    https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html
    Sends an email utilizing Amazon SES  

    Parameters
    ----------
    sender: str  
        Email address to send from  
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
    # Create a new SES resource and specify a region.
    client = boto3.client("ses")
    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={"ToAddresses": [recipient,],},
            Message={
                "Body": {"Text": {"Charset": "UTF-8", "Data": body},},
                "Subject": {"Charset": "UTF-8", "Data": subject},
            },
            Source=sender,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return False
    print("Email sent!"),
    return True

