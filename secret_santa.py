#!/usr/bin/python3
#
#   Andy Gnias
#
#   secret_santa.py - Informs Secret Santa participants of their Secret Santa
#   via email, making it blind from the person running the code.
#
#   Kubuntu 5.13.5
#   Python 3.6.7
#

import sys
import smtplib
from random import shuffle
import getopt
from getpass import getpass
import pathlib
import re as regex

def process_commandline_parameters():
   """
   Processes commandline parameters for dynamic use of email, password, and csv file containing 
   names and emails. Not adaptable to other scripts in its hard-coded form.
   Input: None (hard-coded with the function)
   Output: email,password,fname as strings
   """
   try:
      options, arguments = getopt.getopt(sys.argv[1:], "e:p:n:x:d:", ["email=", "password=", "names=", "exceptions=", "date="])
   except getopt.GetoptError as err:
      print(err)
      exit(1)
   for o, a in options:
      if o in ("-e", "--email"):
         email = a
      elif o in ("-p", "--password"): 
         password = a
      elif o in ("-n", "--names"):
         names_fname = a
      elif o in ("-x", "--exceptions"):
         exceptions_fname = a
      elif o in ("-d", "--date"):
         exchange_date = a
      else:
         print("Unhandled option; ignoring {1}", o)
   try: email
   except:
      email = input("Sender's email: ").strip()
   try: password
   except:
      password = getpass("Password for sender's email: ").strip()
   try: names_fname
   except: 
      generic_names_file = pathlib.Path("names.csv")
      if generic_names_file.is_file(): 
         print("Using names.csv from cwd")
         names_fname = "names.csv"
      else:
         names_fname = input("File containing names,emails: ").strip()
   try: exceptions_fname
   except:
      generic_exceptions_file = pathlib.Path("exceptions.csv")
      if generic_exceptions_file.is_file():
         print("Using exceptions.csv from cwd")
         exceptions_fname = "exceptions.csv"
      else:
         confirmE = input("No exceptions file provided (-x). Would you like to use one? ").strip()
         if regex.match("[Yy]",confirmE):
            exceptions_fname = input("File name: ").strip()
         else:
            exceptions_fname = None
   try: exchange_date
   except:
      confirmD = input("Would you like to specify an exchange date?").strip()
      if regex.match("[Yy]",confirmD):
         exchange_date = input("Specify date however you would like it displayed: ").strip()
      else:
         exchange_date = None
   return email,password,names_fname,exceptions_fname,exchange_date

def generate_names_dictionary(fname):
   """
   Generates a dict of the form d[name] = email from a text file.
   Input: text file name in cwd
   Output: populated dictionary
   """
   d = dict()
   with open(fname,'r') as f:
      for line in f:
         contents = line.strip().split(',')
         name = contents[0].strip()
         email = contents[1].strip()
         d[name] = email
   f.close()
   return d

def generate_exceptions_dict(fname):
   """
   Generates a dictionary of dictionaries where each entry is a dict of the form:
      d[Name] = List of names they can't be matched with
   Input: file name of exceptions
   Return Value: dictionary of dictionaries
   """
   if fname is None:
      return None
   d = dict()
   with open(fname,'r') as f:
      for line in f:
         contents = line.strip().split(',')
         i = 0
         l = list()
         for ex in contents:
            if i == 0:
               name = ex.strip()
            else:
               l.append(ex.strip())
            i += 1
         d[name] = l
         name = contents[0].strip()
   f.close()
   return d

def Make_Selections(names, exceptions, upper_limit = 1000):
   """
   Makes the Secret Santa selections
   Input: Names in a list, exceptions dict, upper limit of attempts to sort (default is 1000)
   Output: None; names list is mutated
   """
   list_sorted = False
   counter = 0
   while not list_sorted and counter < upper_limit: #shuffle list until it abides by conditions set
      counter += 1
      shuffle(names)
      list_sorted = check_conditions(names, exceptions)
   return list_sorted

def check_conditions(nlist, exceptionsDict):
   """
   Prevents people who shouldn't get each other from getting each other
   ex. couples.
   """
   for i in range(len(nlist)):
      name = nlist[i]
      if name in exceptionsDict:
         exceptions = exceptionsDict[name]
         if i == 0:
            if nlist[len(nlist)-1] in exceptions:
               return False
         else:
            if nlist[i-1] in exceptions:
               return False
   return True

def compose_message(gifter, recipient, exchange_date):
   """
   Generates the content of the Secret Santa email.
   Input: gifter, recipient, exchange date (can be none)
   Output: message compatible with smtp email
   """
   subject = "Secret Santa Assignment"
   Assignment = "{}, \n\nYou have been assigned to be {}'s Secret Santa!".format(gifter, recipient)
   Exchange = ""
   if exchange_date is not None: 
      Exchange = " Please purchase a gift for them before the gift exchange on {}.".format(exchange_date)
   body = Assignment + Exchange
   message = 'Subject: {}\n\n{}'.format(subject, body)
   return message

def send_email(from_address, from_password, gifter_email, gifter, recipient, exchange_date):
   """
   Sends Secret Santa email
   Input: Email address to send from, password of email address, email address to send to, gifter's name, recipient's
   name, exchange date as a string or None
   Output: True upon successful completion, else false
   Note: Successful execution of the function does not necessarily mean that an email was sent
   """
   message_body = compose_message(gifter, recipient, exchange_date)
   try:  
      server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
      server.ehlo()
      server.login(from_address, from_password)
      server.sendmail(from_address, gifter_email, message_body)
      server.close()
      print('Email sent!')
   except:  
      print("Error sending email to {}".format(gifter_email))
      return False
   return True

def email_participants(names_list, names_dict, email, password, exchange_date):
   """
   Informs participants who they have for Secret Santa via email
   Input: Names as a list, dict of d[name] = email, email address to send from, password of email address, exchange date
   as a string or None
   Output: True upon completion
   """
   #first person gifts to last name in 'names list
   gifter = names_list[0]
   gifter_email = names_dict[gifter]
   recipient = names_list[len(names_list)-1]
   send_email(email,password,gifter_email,gifter,recipient,exchange_date)
   #everyone else gifts to the person above them in names_list
   for i in range(len(names_list)-1):
      gifter = names_list[i+1]
      gifter_email = names_dict[gifter]
      recipient = names_list[i]
      send_email(email,password,gifter_email,gifter,recipient,exchange_date)
   return True

def main():
   email,password,fname,exceptions_fname,exchange_date = process_commandline_parameters()
   names_dictionary = generate_names_dictionary(fname)
   exceptions_dictionary = generate_exceptions_dict(exceptions_fname)
   names_list = list(names_dictionary.keys())
   check_success = Make_Selections(names_list, exceptions_dictionary) #The Algorithm
   if not check_success:
      print("Secret Santa selections were unable to be made with the inputs provided")
      exit()
   email_participants(names_list, names_dictionary, email, password, exchange_date)

main()
