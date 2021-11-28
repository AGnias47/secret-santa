#!/usr/bin/python3
#
#    Andy Gnias
#
#    test_main.py - Tests script functionality without sending emails
#
#    Kubuntu 5.16.5
#    Python 3.7.5
#

import sys

sys.path.append(".")
from secret_santa import secret_santa


if __name__ == "__main__":
    names_dictionary, addresses_dictionary = secret_santa.generate_names_dictionaries("user_test/names.csv")
    exceptions_dictionary = secret_santa.generate_exceptions_dict("user_test/exceptions.csv")
    names_list = list(names_dictionary.keys())
    check_success = secret_santa.make_selections(names_list, exceptions_dictionary)  # The Algorithm
    if not check_success:
        sys.exit("Secret Santa selections were unable to be made with the inputs provided")
    secret_santa.email_participants(names_list, names_dictionary, addresses_dictionary, None, None, True)
