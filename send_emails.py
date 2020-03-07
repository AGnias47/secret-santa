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


def send_gmail_smtp_email(sender, recipient, subject, body):
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

