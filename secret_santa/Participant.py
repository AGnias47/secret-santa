ENCODING = "UTF-8"


class Participant:
    def __init__(self, name, email, address=None):
        """
        Initialize a participant

        Parameters
        ----------
        name: str
        email: str
        address: str or None
        """
        self.name = name
        self.email = email
        self.address = address
        self.exceptions = list()

    def __eq__(self, p):
        return self.name == p.name

    def __lt__(self, p):
        return self.name < p.name

    def __str__(self):
        return self.name


def create_participant_hash(names, exceptions=None):
    """
    Generate a hash table of participants
    Key: Name
    Value: Corresponding Participant object

    Parameters
    ----------
    names: str
    Path to CSV containing participant information in the form:
        name,email,address(optional)
    exceptions: str
    Path to CSV containing exceptions (optional). Format is:
        name, exception_1, exception_2, ..., exception_n

    Returns
    -------
    dict
    """
    participants = dict()
    with open(names, "r", encoding=ENCODING) as f:
        for line in f:
            contents = line.strip().split(",")
            name = contents[0].strip()
            email = contents[1].strip()
            try:
                address = ",".join(contents[2:]).strip()
                if address == "":
                    address = None
                participants[name] = Participant(name, email, address)
            except IndexError:
                participants[name] = Participant(name, email)
    f.close()
    if exceptions:
        with open(exceptions, "r", encoding=ENCODING) as f:
            for line in f:
                contents = line.strip().split(",")
                name = contents[0]
                for ex in contents[1:]:
                    participants[name].exceptions.append(participants[ex.strip()])
        f.close()
    return participants
