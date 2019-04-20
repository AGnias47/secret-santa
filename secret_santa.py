#!/usr/bin/python3
#
#   Andy
#
#   secret_santa.py - Informs Secret Santa participants of their Secret Santa
#   via email, making it blind from the person running the code.
#
#   4/14/2019
#
#   Kubuntu 5.13.5
#   Python 3.4.2
#

import sys
import smtplib
from random import shuffle
import getopt
from getpass import getpass
import pathlib
import re

def process_commandline_parameters() :
	"""Processes commandline parameters for dynamic use of email, password, and csv file containing 
	names and emails. Not adaptable to other scripts in its hard-coded form.
	Input: None (hard-coded with the function)
	Output: email,password,fname as strings"""
	try :
		options, arguments = getopt.getopt(sys.argv[1:], "e:p:t:x:", ["email=", "password=", "textfile=", "exceptions="])
	except getopt.GetoptError as err:
		print(err)
		exit(1)
	for o, a in options :
		if o in ("-e", "--email") :
			email = a
		elif o in ("-p", "--password") : 
			password = a
		elif o in ("-t", "--textfile") :
			fname = a
		elif o in ("-x", "--exceptions") :
			exceptions = a
		else :
			print("Unhandled option; ignoring {1}", o)
	try : email
	except :
		email = input("Sender's email: ").strip()
	try : password
	except :
		password = getpass("Password for sender's email: ").strip()
	try : fname
	except : 
		generic_names_file = pathlib.Path("names.csv")
		if generic_names_file.is_file() : 
			print("Using names.csv from cwd")
			fname = "names.csv"
		else :
			fname = input("File containing names,emails : ").strip()
	try : exceptions_fname
	except :
		generic_exceptions_file = pathlib.Path("exceptions.txt")
		if generic_exceptions_file.is_file() :
			print("Using exceptions.txt from cwd")
			exceptions_fname = "exceptions.txt"
		else :
			confirmE = input("No exceptions file provided (-x). Would you like to use one? ").strip()
			if re.match(r"[Yy]*",confirmE) :
				exceptions_fname = input("File name: ").strip()
	return email,password,fname,exceptions_fname

def generate_names_dictionary(fname) :
	"""Generates a dict of the form d[name] = email from a text file.
	Input: text file name in cwd
	Output: populated dictionary"""
	d = dict()
	with open(fname,'r') as f :
		for line in f :
			contents = line.strip().split(',')
			name = contents[0].strip()
			email = contents[1].strip()
			d[name] = email
	f.close()
	return d

def generate_exceptions_dict(fname) :
	"""Generates a dictionary of dictionaries where each entry is a dict of the form:
		d[Name] = List of names they can't be matched with
	Input: file name of exceptions
	Return Value: dictionary of dictionaries
	"""
	d = dict()
	with open(fname,'r') as f :
		for line in f :
			contents = line.strip().split(',')
			i = 0
			l = list()
			for ex in contents :
				if i == 0 :
					name = ex.strip()
				else :
					l.append(ex.strip())
				i += 1
			d[name] = l
			name = contents[0].strip()
	f.close()
	return d

def check_conditions(nlist, exceptionsDict) :
	"""Prevents people who shouldn't get each other from getting each other
	i.e. couples."""
	for i in range(len(nlist)) :
		name = nlist[i]
		if name in exceptionsDict :
			exceptions = exceptionsDict[name]
			if i == 0 :
				if nlist[len(nlist)-1] in exceptions :
					return False
			else :
				if nlist[i-1] in exceptions :
					return False
	return True

def compose_message(gifter, recipient) :
    """Composes body of Secret Santa email"""
    exchange_date = "December 21, 2018"
    subject = "Secret Santa 2018"
    body = ("{}, \n\nYou have been assigned to be {}'s Secret Santa! Please purchase a gift for them before \
the gift exchange on {}".format(gifter, recipient, exchange_date))
    message = 'Subject: {}\n\n{}'.format(subject, body)
    return message

def test_message() :
    """Generic message to test everyone's emails."""
    subject = "Secret Santa 2018"
    body = "Hello!\n\nThis is a test of the Secret Santa assignment system.\
To confirm that you are able to receive this email, please let Andy \
know that you have received this message by replying directly to this \
email."
    message = 'Subject: {}\n\n{}'.format(subject, body)
    return message

def send_email(from_address,from_password,gifter_email,gifter,recipient) :
	"""Sends Secret Santa email"""
	#message_body = test_message()
	message_body = compose_message(gifter,recipient)
	try:  
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(from_address, from_password)
		server.sendmail(from_address, gifter_email, message_body)
		server.close()
		print('Email sent!')
	except:  
		print("Error sending email to {}".format(gifter_email))

def main() :
	email,password,fname,exceptions_fname = process_commandline_parameters()
	d = generate_names_dictionary(fname)
	exceptions_dict = generate_exceptions_dict(exceptions_fname)
	names = list(d.keys())
	list_sorted = False
	while not list_sorted : #shuffle list until it abides by conditions set
		shuffle(names)
		list_sorted = check_conditions(names, exceptions_dict)
	print(names)

	#first person gifts to last name in 'names list
	gifter = names[0]
	gifter_email = d[gifter]
	recipient = names[len(names)-1]
	send_email(email,password,gifter_email,gifter,recipient)
	#everyone else gifts to the person above them in 'names' list
	for i in range(len(names)-1) :
		gifter = names[i+1]
		gifter_email = d[gifter]
		recipient = names[i]
		send_email(email,password,gifter_email,gifter,recipient)

main()
