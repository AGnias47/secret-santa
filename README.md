# Secret Santa Selection Manager
Python script to manage Secret Santa selections. Makes selections, and then alerts participants of who they are assigned
to give a gift to via email.

## Requirements
 * Python 3
 * Method for sending emails (ex. Gmail account)


## Usage
```
wget https://github.com/AGnias47/Secret_Santa/blob/master/secret_santa.py
python3 secret_santa.py -e sender@email.com -n names.csv -x exceptions.csv -d "12/25/2020"
```


## Inputs
### -e or --email
Email from which all participant emails will be sent. If not provided, will be prompted for on the command line.

### -p or --password
Password for the provided email. If not provided, will be prompted for on the command line. Password input will be masked.

### -n or --names
Flat file containing the Secret Santa participant's names and emails in the form:

```
Name,Email
```

If not provided, the script will look for "names.csv" in the cwd and will use it if it exists. If not, will prompt the user for a filename.

See "names.csv" in this repo for an example.

### -x or --exceptions (optional parameter)
Flat file containing pairings which should not occur in the form:

```
Person A, Person 1 who should not be assigned to A, Person 2 who should not be assigned to A, ..., Person n who should not be assigned to A
```

Note that if A should not get B and B should not get A, both of these exceptions must be provided, i.e. saying A should not get B does not mean B cannot get A.

If not provided, the script will look for "exceptions.csv" in the cwd and will use it if it exists. If not, will ask the user if they would like to use an exceptions file. If they type anything starting with the letter y, (ex. yes or Y), the user will be prompted for the name of the exceptions file. If not, the script will continue without any exceptions.

See "exceptions.csv" in this repo for an example.

### -d or --date (optional parameter)
Date when the Secret Santa gift exchange will occur. If not provided, script will ask if the user would like to provide
an exchange date, using the same method (Y or yes) as the exclusions list question.

If provided, the exchange date will be included in the email alerting participants of who their secret santa is. If not,
no date will be provided in the email sent to the participant.


## Functionality Description
### Function Documentation
[Function Documentation generated from docstrings using pdoc](function_definitions.html)

### The Algorithm
While effective in most situations, the method for selecting Secret Santa pairs is relatively unsophisticated. The program will take the list of names and put them in a random order using the Python shuffle method, which utilizes the [Fisher-Yates shuffle and runs in O(n) time](https://softwareengineering.stackexchange.com/questions/215737/how-python-random-shuffle-works). Random numbers for this shuffle are generated using a [Wichman-Hill random number generator](https://en.wikipedia.org/wiki/Wichmann%E2%80%93Hill). Using this list, the first person in the list is assigned to give a gift to the last person in the list, and everyone else is assigned to give a gift to the person before them. Note that with this implementation, there are no closed cycles of gift giving, i.e. a scenario where A gives to B and B gives to A will never occur in a list with more than 2 names.

After the list of names is shuffled, the program will perform a check to ensure that no invalid pairings have been made, ex. someone is paired with someone on their exclude list. If an invalid paring is made, the shuffle is performed again. This process is repeated until a valid sort is performed. 

Note that this method could lead to long program runtimes if given a large list of names with many inter-connected exclusions, and would also run infinitely if a scenario was given in which no valid set of parings could be made. To prevent an infinite run time, a maximum number of iterations is currently set by default (10000) and can be overridden by modifying the program. However, the program should suit most scenarios. Runtime for a group of ~15 people has always completed seemingly instantaneously during the work of this algorithm, so at this time there are no plans to improve it.

### Sending Emails
Emails are currently sent through the Simple Mail Transfer Protocol using Python's smtplib. Since SMTP is open to man in
the middle attacks, common email servers, such as gmail, will fail to send an email using this script by default because
it poses a security risk. In Gmail, you can work around this by logging into your Gmail account and going to
[https://myaccount.google.com/lesssecureapps](https://myaccount.google.com/lesssecureapps), and enabling it while the 
script runs. The current method of running this script has been to allow less secure apps via Gmail, run the script, and 
then continue blocking less secure apps, which limits the time exposed to less secure apps to a minimum. See the Future
Work section for plans to move away from SMTP.

## Future Work
Based on usage from the last Secret Santa, I'm going to attempt to utilize AWS or some other email service to send out
emails. Using SMTP via Gmail sent the emails to my participants' spam folders, which was not ideal.

