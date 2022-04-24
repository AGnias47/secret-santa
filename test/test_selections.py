#!/usr/bin/env python3

from secret_santa.Participant import create_participant_hash
from secret_santa.selections import make_selections

import random
import pytest

random.seed(42)


def test_make_selections():
    participants = create_participant_hash("test/names.csv", "test/exceptions.csv")
    selections = make_selections(participants)
    assert ["Andy", "Camille", "Daryl", "Elias", "Bill"] == selections


if __name__ == "__main__":
    pytest.main()
