from send_email.gmail_smtp import send_email


class Email:
    def __init__(self, username, password, send_email_function=send_email):
        self._email = (username, password)
        self._send_email = send_email_function

    def email_participants(self, participants, exchange_date=None):
        """
        Informs participants who they have for Secret Santa via email

        Parameters
        ----------
        participants: list(Participants)
            List of Participants
        exchange_date: str (default is None)
            Date of the gift exchange; can be None if exchange date is undecided

        Returns
        -------
        list
            List of return values (True or False) from sending emails to participants

        """
        subject = "Secret Santa Assignment"
        sent_emails_boolean_list = list()
        # first person gifts to last name in 'names list
        gifter = participants[0]
        recipient = participants[len(participants) - 1]
        # compose a message based on the selected gifter and recipient
        message_body = compose_message_body(gifter, recipient, exchange_date)
        status = self._send_email(self._email, gifter.email, subject, message_body)
        sent_emails_boolean_list.append(status)
        # everyone else gifts to the person above them in names_list
        for i, participant in enumerate(participants):
            if i == (len(participants) - 1):  # All gifts processed; prevents out of range error
                continue
            gifter = participants[i + 1]
            recipient = participants[i]
            message_body = compose_message_body(gifter, recipient, exchange_date)
            status = self._send_email(self._email, gifter.email, subject, message_body)
            sent_emails_boolean_list.append(status)
        return sent_emails_boolean_list


def compose_message_body(gift_giver, recipient, exchange_date=None):
    """
    Generates the content of the Secret Santa email.

    Parameters
    ----------
    gift_giver: Participant
        Name of gift giver
    recipient: Participant
        Name of gift recipient
    exchange_date: str (default is None)
        If provided, specifies the exchange date in the message

    Returns
    -------
    str
        Message compatible with SMTP email

    """
    message = f"{gift_giver.name}, \n\nYou have been assigned to be {recipient.name}'s Secret Santa!"
    if exchange_date:
        message += " Please purchase a gift for them before the gift exchange on {}.".format(exchange_date)
    if recipient.address:
        message += f" If you are unable to give them the gift in person or at the gift exchange, please send a gift to them at {recipient.address}."
    return message

