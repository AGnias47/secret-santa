# Secret Santa Selection Manager

Python program to manage Secret Santa selections. Makes selections, and then alerts participants of who they are assigned
to give a gift to via email.

## Requirements
### General Requirements
 * Python 3
 * Method for sending emails (ex. Amazon SES, Gmail account)


## Usage
```
wget https://github.com/AGnias47/Secret_Santa/blob/master/secret_santa.py
python3 main.py -e sender@email.com -n names.csv -x exceptions.csv -d "12/25/2020"
```


## Inputs

### -e or --email

Email from which all participant emails will be sent. If not provided, will be prompted for on the command line.

### -p or --password (Note: only used with Gmail SMTP)

Password for the provided email. If not provided, will be prompted for on the command line. Password input will be masked.

### -n or --names

Flat file containing the Secret Santa participant's names and emails in the form:

```
Name,Email
```

If not provided, the script will look for "names.csv" in the cwd and will use it if it exists. If not, will prompt the user for a filename.

See "test/names.csv" in this repo for an example.

### -x or --exceptions (optional parameter)

Flat file containing pairings which should not occur in the form:

```
Person A, Person 1 who should not be assigned to A, Person 2 who should not be assigned to A, ..., Person n who should not be assigned to A
```

Note that if A should not get B and B should not get A, both of these exceptions must be provided, i.e. saying A should not get B does not mean B cannot get A.

If not provided, the script will look for "exceptions.csv" in the cwd and will use it if it exists. If not, will ask the user if they would like to use an exceptions file. If they type anything starting with the letter y, (ex. yes or Y), the user will be prompted for the name of the exceptions file. If not, the script will continue without any exceptions.

See "test/exceptions.csv" in this repo for an example.

### -d or --date (optional parameter)

Date when the Secret Santa gift exchange will occur. If not provided, script will ask if the user would like to provide
an exchange date, using the same method (Y or yes) as the exclusions list question.

If provided, the exchange date will be included in the email alerting participants of who their secret santa is. If not,
no date will be provided in the email sent to the participant.

### The Algorithm

While relatively unsophisticated, the method for selecting Secret Santa pairs is effective in most situations. The program will take the list of names and put them in a random order using the Python shuffle method, which utilizes the [Fisher-Yates shuffle and runs in O(n) time](https://softwareengineering.stackexchange.com/questions/215737/how-python-random-shuffle-works). Random numbers for this shuffle are generated using a [Wichman-Hill random number generator](https://en.wikipedia.org/wiki/Wichmann%E2%80%93Hill). Using this list, the first person in the list is assigned to give a gift to the last person in the list, and everyone else is assigned to give a gift to the person before them. Note that with this implementation, there are no closed cycles of gift giving, i.e. a scenario where A gives to B and B gives to A will never occur in a list with more than 2 names.

After the list of names is shuffled, the program will perform a check to ensure that no invalid pairings have been made, ex. someone is paired with someone on their exclude list. If an invalid paring is made, the shuffle is performed again. This process is repeated until a valid sort is performed. 

Note that this method could lead to long program runtimes if given a large list of names with many inter-connected exclusions, and would also run infinitely if a scenario was given in which no valid set of parings could be made. To prevent an infinite run time, a maximum number of iterations is currently set by default (10000) and can be overridden by modifying the program. However, the program should suit most scenarios. Runtime for a group of ~15 people has always completed seemingly instantaneously during the work of this algorithm, so at this time there are no plans to improve it.

### Sending Emails

Emails are currently sent through SMTP using gmail. More secure methods may be implemented in a future release.

#### Gmail SMTP

Emails sent through Gmail are currently sent through the Simple Mail Transfer Protocol using Python's smtplib. Since
SMTP is open to man-in-the-middle attacks, common email servers, such as gmail, will fail to send an email using this script by default because
it poses a security risk. In Gmail, you can work around this by logging into your Gmail account and going to
[https://myaccount.google.com/lesssecureapps](https://myaccount.google.com/lesssecureapps), and enabling it while the 
script runs. The current method of running this script using Gmail has been to allow less secure apps via Gmail, run the script, and 
then continue blocking less secure apps, which limits the time exposed to less secure apps to a minimum. To avoid this,
it is recommended to use Amazon SES.

## Proposed Updates

* A better algorithm
    * Will likely utilize perfect matching in a graph. [Paths, Trees, and Flowers](https://math.nist.gov/~JBernal/p_t_f.pdf) was recommended in a Stackoverflow post so I'll likely look into that
* React frontend
* More secure method of sending emails
* Sphinx documentation

