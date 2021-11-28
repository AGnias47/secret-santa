#!/usr/bin/env python3

import pytest
from secret_santa.secret_santa import generate_names_dictionaries, generate_exceptions_dict, make_selections


def test_generate_names_dictionaries():
    names_and_emails, names_and_addresses = generate_names_dictionaries("test/names.csv")
    assert names_and_emails["Andy"] == "andy@aol.com"
    assert names_and_emails["Bill"] == "bill@html.com"
    assert names_and_emails["Camille"] == "Cam@aol.com"
    assert names_and_emails["Daryl"] == "Daryl@gmail.com"
    assert names_and_emails["Elias"] == "elias@gmail.com"
    assert names_and_addresses["Andy"] == "123 Main Street, King of Prussia, PA 19406"
    assert names_and_addresses["Bill"] is None
    assert names_and_addresses["Camille"] == "45 A Rockefeller Plaza, New York, NY 10096"
    assert names_and_addresses["Daryl"] is None
    assert names_and_addresses["Elias"] is None


def test_generate_exceptions_dict_no_file():
    assert generate_exceptions_dict(None) is None


def test_generate_exceptions_dict():
    exceptions = generate_exceptions_dict("test/exceptions.csv")
    assert 2 == len(exceptions)
    assert ["Elias", "Daryl"] == exceptions["Andy"]
    assert ["Andy"] == exceptions["Elias"]


def test_make_selections():
    names_and_emails, names_and_addresses = generate_names_dictionaries("test/names.csv")
    exceptions = generate_exceptions_dict("test/exceptions.csv")
    assert make_selections(list(names_and_emails.keys()), exceptions)


if __name__ == "__main__":
    pytest.main()
