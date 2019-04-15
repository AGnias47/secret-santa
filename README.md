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
