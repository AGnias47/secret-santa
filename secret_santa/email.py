from send_email.gmail_smtp import send_email


class Email:
    def __init__(self, username, password, send_email_function=send_email):
        self._email = (username, password)
        self._send_email = send_email_function

    def email_participants(self, participants, order, exchange_date=None, subject="Secret Santa Assignment"):
        """
        Informs participants who they have for Secret Santa via email

        Parameters
        ----------
        participants: dict
            Hash table containing participants
        order: list
            Names in randomized order where order[i] = gift giver, order[i+1] = recipient (n+1 = 0)
        exchange_date: str (default is None)
            Date of the gift exchange; can be None if exchange date is undecided
        subject: str (Default is "Secret Santa Assignment")
            Subject of the email
        Returns
        -------
        list
            List of return values (True or False) from sending emails to participants

        """
        sent_emails_boolean_list = list()
        # everyone gifts to the person above them in names_list, first person gifts to last
        for i, _ in enumerate(order):
            gift_giver = participants[order[(i + 1) % len(order)]]
            recipient = participants[order[i]]
            message_body = compose_message_body(gift_giver, recipient, exchange_date)
            status = self._send_email(self._email, gift_giver.email, subject, message_body)
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
        message += f" Please purchase a gift for them before the gift exchange on {exchange_date}."
    if recipient.address:
        message += (
            f" If you are unable to give them the gift in person or at the "
            f"gift exchange, please send a gift to them at {recipient.address}."
        )
    return message
