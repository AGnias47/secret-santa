# Secret_Santa
Python script to manage Secret Santa selections

## Inputs
### -e or --email
Email from which all participant emails will be sent. If not provided, will be prompted for on the command line.

### -p or --password
Password for the provided email. If not provided, will be prompted for on the command line. Password input will be
masked.

### -t or --textfile
File containing the Secret Santa participant's names and emails in the form:

```
Name,Email
```

If not provided, will look for "names.csv" in the cwd and will use if it exists. If not, will prompt the user for a
filename.

### -x or --exceptions (optional parameter)
File containing pairings which should not occur in the form:

```
Person A, Person 1 who should not be assigned to A, Person 2 who should not be assigned to A, ..., Person n who should
not be assigned to A
```

If
## Input Flat Files

## The Algorithm
While effective in most situations, the method for selecting Secret Santa pairs is relatively unsophisticated. The
program will take the list of names and put them in a random order using the Python shuffle method, which utilizes the
Fisher-Yates shuffle running in O(n) time (Source:
https://softwareengineering.stackexchange.com/questions/215737/how-python-random-shuffle-works). Using this list, the
first person in the list is assigned to give a gift to the last person in the list, and everyone else is assigned to
give a gift to the person before them. Note that with this implementation, there are no closed cycles of gift giving,
i.e. a scenario where A gives to B and B gives to A will never occur in a list with more than 2 names.

After the list of names is shuffled, the program will perform a check to ensure that no invalid pairings have been made, i.e. someone is paired
with someone on their exclude list. If an invalid paring is made, the shuffle is performed again. This process is
repeated until a valid sort is performed. 

Note that this method could lead to long program runtimes if given a large list of names with many inter-connected
solutions, and would also run infinitely if a scenario was given in which no valid set of parings could be made.
However, the program should suit most scenarios. Runtime for a group of ~15 people has always completed seemingly
instantaneously during the work of this algorithm, so at this time there are no plans to improve it.
