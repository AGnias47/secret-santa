#!/bin/bash
#
#   A. Gnias
#
#   Kubuntu 5.16.5
#   GNU bash, version 5.0.3(1)-release

./test_commandline_parsing.py --ses -e test@email.com -p passwd -d _date
./test_commandline_parsing.py --gmail -e test@email.com -p passwd -d _date
./test_commandline_parsing.py --ses --email test@email.com --password passwd --date _date
./test_commandline_parsing.py --gmail --email test@email.com --password passwd --date _date

./test_commandline_parsing.py --ses -e test@email.com -p passwd -d _date -n names_file 
./test_commandline_parsing.py --gmail -e test@email.com -p passwd -d _date -n names_file 
./test_commandline_parsing.py --ses --email test@email.com --password passwd --date _date --names names_file 
./test_commandline_parsing.py --gmail --email test@email.com --password passwd --date _date --names names_file 

./test_commandline_parsing.py --ses -e test@email.com -p passwd -d _date -e exceptions_file
./test_commandline_parsing.py --gmail -e test@email.com -p passwd -d _date -e exceptions_file
./test_commandline_parsing.py --ses --email test@email.com --password passwd --date _date --exceptions exceptions_file
./test_commandline_parsing.py --gmail --email test@email.com --password passwd --date _date --exceptions exceptions_file

./test_commandline_parsing.py --ses -e test@email.com -p passwd -d _date -n names_file -e exceptions_file
./test_commandline_parsing.py --gmail -e test@email.com -p passwd -d _date -n names_file -e exceptions_file
./test_commandline_parsing.py --ses --email test@email.com --password passwd --date _date --names names_file --exceptions exceptions_file
./test_commandline_parsing.py --gmail --email test@email.com --password passwd --date _date --names names_file --exceptions exceptions_file


