#!/usr/bin/env python3

"""
Secret Santa Selection Algorithm
"""

from random import shuffle


def make_selections(participants, upper_limit=10000):
    """
    Makes the Secret Santa selections

    Parameters
    ----------
    participants: dict
        Hash table containing participants
    upper_limit: int (default is 10000)
        Max sorting attempts to execute

    Raises
    ------
    RuntimeError: Raised if no valid order can be found

    Returns
    -------
    list
        Order of names for Secret Santa
    """
    order = list(participants.keys())
    list_sorted = False
    counter = 0
    while not list_sorted and counter < upper_limit:  # shuffle list until integration_test abides by conditions set
        counter += 1
        shuffle(order)
        list_sorted = check_conditions(order, participants)
    if list_sorted:
        return order
    else:
        raise RuntimeError("Secret Santa selections were unable to be made with the inputs provided")


def check_conditions(order, participants):
    """
    Check to prevent people who shouldn't get each other from getting each other, ex. couples

    Parameters
    ----------
    order: list
        Name order of Participants
    participants: dict
        Hash table containing participants

    Returns
    -------
    bool
        True if no exceptions are violated, else False

    """
    if all(p.exceptions is None for p in list(participants.values())):
        return True
    for i, p in enumerate(order):
        if participants[p].exceptions and participants[order[i - 1]] in participants[p].exceptions:
            return False
    return True
