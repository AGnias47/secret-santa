#!/usr/bin/env python3

from secret_santa.Participant import create_participant_hash
from secret_santa.selections import make_selections

import pytest


def test_make_selections():
    participants = create_participant_hash("test/names.csv", "test/exceptions.csv")
    assert type(make_selections(participants)) == list


if __name__ == "__main__":
    pytest.main()
