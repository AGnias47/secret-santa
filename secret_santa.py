#!/usr/bin/env python
#
#	A. Gnias
#
#	secret_santa.py - Informs Secret Santa participants of their Secret Santa
#	via email, making it blind from the person running the code.
#
#	10/01/2016
#
#	Ubuntu Linux 3.4.0+
#	Python 2.7.6
#
import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from random import shuffle

def compose_message(gifter, recipient) :
	"""Composes body of Secret Santa email"""
	exchange_date = "December 27, 2016"
 	return "%s,\n\tYou have been assigned to be %s's Secret Santa! Please \
purchase a gift for them before the gift exchange on \
%s."%(gifter,recipient,exchange_date)

def test_message(gifter, recipient) :
	"""Generic message to test everyone's emails."""
	return "Hello!\n\tThis is a test of the Secret Santa assignment system.\
To confirm that you are able to receive this email, please let Andy Gnias \
know that you have received this message by replying directly to this \
email."

def send_email(from_address,from_password,gifter_email,gifter,recipient) :
	"""Sends Secret Santa email"""
	message = MIMEMultipart()
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.starttls()
	server.login(from_address,from_password)
	message['From'] = from_address
	message['To'] = gifter_email
	message['Subject'] = "Secret Santa 2016!"
	message_body = compose_message(gifter,recipient)
	message.attach(MIMEText(message_body, 'plain'))
	text = message.as_string()
	server.sendmail(from_address, gifter_email, text)
	server.quit()

def check_conditions(nlist) :
	"""Prevents people who shouldn't get each other from getting each other
	i.e. couples."""
	for i in range(len(nlist)) :
		first = i
		second = i+1
		if second == len(nlist) :
			second = 0
		if nlist[first] == "Andy" and nlist[second] == "Drew" or \
		nlist[first] == "Drew" and nlist[second] == "Andy" :
			return False
	return True

def main() :
	argc = len(sys.argv)

	from_address = "email@gmail.com"
	if argc == 1 :
		print "Requires %s email password as argument"%from_address
		sys.exit()

	from_password = sys.argv[1]

	d = dict()
#	d["Andy"] = "email@gmail.com"
#	continue in same form for other patricipants
	names = d.keys()
	list_sorted = False
	while not list_sorted :
		shuffle(names)
		list_sorted = check_conditions(names)

	print names

	#first person gifts to last name in 'names list
	gifter = names[0]
	gifter_email = d[gifter]
	recipient = names[len(names)-1]
	send_email(from_address,from_password,gifter_email,gifter,recipient)
	#everyone else gifts to the person above them in 'names' list
	for i in range(len(names)-1) :
		gifter = names[i+1]
		gifter_email = d[gifter]
		recipient = names[i]
		send_email(from_address,from_password,gifter_email,gifter,recipient)

main()
