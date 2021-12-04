#!/usr/bin/env python3

from secret_santa.Participant import Participant, create_participant_hash

import pytest


def test_init():
    p = Participant("Andy", "andy@aol.com", "123 Main Street, Fort Collins, CO")
    assert p.name == "Andy"
    assert p.email == "andy@aol.com"
    assert p.address == "123 Main Street, Fort Collins, CO"


def test_create_participant_hash():
    participant_hash = create_participant_hash("test/names.csv")
    assert participant_hash["Andy"].name == "Andy"
    assert participant_hash["Bill"].name == "Bill"
    assert participant_hash["Camille"].name == "Camille"
    assert participant_hash["Daryl"].name == "Daryl"
    assert participant_hash["Elias"].name == "Elias"
    assert participant_hash["Andy"].email == "andy@aol.com"
    assert participant_hash["Bill"].email == "bill@html.com"
    assert participant_hash["Camille"].email == "Cam@aol.com"
    assert participant_hash["Daryl"].email == "Daryl@gmail.com"
    assert participant_hash["Elias"].email == "elias@gmail.com"
    assert participant_hash["Andy"].address == "123 Main Street, King of Prussia, PA 19406"
    assert participant_hash["Bill"].address is None
    assert participant_hash["Camille"].address == "45 A Rockefeller Plaza, New York, NY 10096"
    assert participant_hash["Daryl"].address is None
    assert participant_hash["Elias"].address is None
    assert participant_hash["Andy"].exceptions == []
    assert participant_hash["Bill"].exceptions == []
    assert participant_hash["Camille"].exceptions == []
    assert participant_hash["Daryl"].exceptions == []
    assert participant_hash["Elias"].exceptions == []


def test_exceptions():
    participant_hash = create_participant_hash("test/names.csv", "test/exceptions.csv")
    assert len(participant_hash["Andy"].exceptions) == 2
    assert participant_hash["Daryl"] in participant_hash["Andy"].exceptions
    assert participant_hash["Elias"] in participant_hash["Andy"].exceptions
    assert participant_hash["Andy"] in participant_hash["Elias"].exceptions


if __name__ == "__main__":
    pytest.main()
