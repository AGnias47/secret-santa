from random import shuffle


def make_selections(participants, upper_limit=10000):
    """
    Makes the Secret Santa selections

    Parameters
    ----------
    participants: list(Participant)
        List of participants
    upper_limit: int (default is 10000)
        Max sorting attempts to execute

    Returns
    -------
    bool
        True if list was properly sorted, else False. Names list is mutated in new shuffled order

    """
    list_sorted = False
    counter = 0
    while not list_sorted and counter < upper_limit:  # shuffle list until it abides by conditions set
        counter += 1
        shuffle(participants)
        list_sorted = check_conditions(participants)
    return list_sorted


def check_conditions(participants):
    """
    Check to prevent people who shouldn't get each other from getting each other, ex. couples

    Parameters
    ----------
    participants: list(Participant)
        List of participants

    Returns
    -------
    bool
        True if no exceptions are violated, else False

    """
    if all(p.exceptions is None for p in participants):
        return True
    for i, participant in enumerate(participants):
        if participant.exceptions and participants[i - 1] in participant.exceptions:
            return False
    return True
