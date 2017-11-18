#!/usr/bin/python3.4
#
#	Andy
#
#	secret_santa.py - Informs Secret Santa participants of their Secret Santa
#	via email, making it blind from the person running the code.
#
#	11/17/2017
#
#  Linux raspberrypi 4.1.7+
#	Python 3.4.2
#

import sys
import smtplib
from random import shuffle

def compose_message(gifter, recipient) :
	"""Composes body of Secret Santa email"""
	exchange_date = "December 20, 2017"
	return ("{}, \n\nYou have been assigned to be {}'s Secret Santa! Please purchase a gift for them before \
the gift exchange on {}".format(gifter, recipient, exchange_date))

def test_message() :
	"""Generic message to test everyone's emails."""
	return "Hello!\n\nThis is a test of the Secret Santa assignment system.\
To confirm that you are able to receive this email, please let Andy Gnias \
know that you have received this message by replying directly to this \
email."

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

def check_conditions(nlist) :
	"""Prevents people who shouldn't get each other from getting each other
	i.e. couples."""
	for i in range(len(nlist)) :
		recp = i
		gifter = i+1
		if gifter == len(nlist) :
			gifter = 0
		if nlist[gifter] == "Secret" and nlist[recp] == "Santa" or \
		nlist[gifter] == "Santa" and nlist[recp] == "Secret" :
			return False
	return True

def main() :
	argc = len(sys.argv)
	from_address = "________@gmail.com"
	if argc == 1 :
		print("Requires {} email password as argument".format(from_address))
		sys.exit()
	from_password = sys.argv[1]

	d = dict() #hash with key=names value=email
	d["Santa"] = "GimmeDemCookies69420@gmail.com"
	#continue in same format for other participants

	names = list(d.keys())
	list_sorted = False
	while not list_sorted : #shuffle list until it abides by conditions set
		shuffle(names)
		list_sorted = check_conditions(names)

	print(names)

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
