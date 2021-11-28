#!/bin/bash
#
#   A. Gnias
#
#   Kubuntu 5.16.5
#   GNU bash, version 5.0.3(1)-release

user_test/command_line_test_helper.py -e test@email.com -p passwd -d _date
user_test/command_line_test_helper.py -e test@email.com -p passwd -d _date
user_test/command_line_test_helper.py --email test@email.com --password passwd --date _date
user_test/command_line_test_helper.py --email test@email.com --password passwd --date _date

user_test/command_line_test_helper.py -e test@email.com -p passwd -d _date -n names_file
user_test/command_line_test_helper.py -e test@email.com -p passwd -d _date -n names_file
user_test/command_line_test_helper.py --email test@email.com --password passwd --date _date --names names_file
user_test/command_line_test_helper.py --email test@email.com --password passwd --date _date --names names_file

user_test/command_line_test_helper.py -e test@email.com -p passwd -d _date -e exceptions_file
user_test/command_line_test_helper.py -e test@email.com -p passwd -d _date -e exceptions_file
user_test/command_line_test_helper.py --email test@email.com --password passwd --date _date --exceptions exceptions_file
user_test/command_line_test_helper.py --email test@email.com --password passwd --date _date --exceptions exceptions_file

user_test/command_line_test_helper.py -e test@email.com -p passwd -d _date -n names_file -e exceptions_file
user_test/command_line_test_helper.py -e test@email.com -p passwd -d _date -n names_file -e exceptions_file
user_test/command_line_test_helper.py --email test@email.com --password passwd --date _date --names names_file --exceptions exceptions_file
user_test/command_line_test_helper.py --email test@email.com --password passwd --date _date --names names_file --exceptions exceptions_file


