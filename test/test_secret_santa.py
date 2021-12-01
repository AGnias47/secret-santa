#!/usr/bin/env python3

from secret_santa.Participant import create_participant_list
from secret_santa.selections import make_selections

import pytest


def get_email(name, participant_list):
    return next(filter(lambda x: x.name == name, participant_list)).email


def get_address(name, participant_list):
    return next(filter(lambda x: x.name == name, participant_list)).address


def get_exceptions(name, participant_list):
    return next(filter(lambda x: x.name == name, participant_list)).exceptions


def test_generate_names_dictionaries():
    participant_list = create_participant_list("test/names.csv")
    assert get_email("Andy", participant_list) == "andy@aol.com"
    assert get_email("Bill", participant_list) == "bill@html.com"
    assert get_email("Camille", participant_list) == "Cam@aol.com"
    assert get_email("Daryl", participant_list) == "Daryl@gmail.com"
    assert get_email("Elias", participant_list) == "elias@gmail.com"
    assert get_address("Andy", participant_list) == "123 Main Street, King of Prussia, PA 19406"
    assert get_address("Bill", participant_list) is None
    assert get_address("Camille", participant_list) == "45 A Rockefeller Plaza, New York, NY 10096"
    assert get_address("Daryl", participant_list) is None
    assert get_address("Elias", participant_list) is None
    assert get_exceptions("Andy", participant_list) is None
    assert get_exceptions("Bill", participant_list) is None
    assert get_exceptions("Camille", participant_list) is None
    assert get_exceptions("Daryl", participant_list) is None
    assert get_exceptions("Elias", participant_list) is None


def test_make_selections():
    participants = create_participant_list("test/names.csv", "test/exceptions.csv")
    assert make_selections(participants)


if __name__ == "__main__":
    pytest.main()
