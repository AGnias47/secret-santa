class Participant:
    def __init__(self, name, email, address=None, exceptions=None):
        self.name = name
        self.email = email
        self.address = address
        self.exceptions = exceptions

    def __eq__(self, p):
        return self.name == p.name

    def __lt__(self, p):
        return self.name < p.name

    def __str__(self):
        return self.name


def create_participant_list(names, exceptions=None):
    participants = list()
    with open(names, "r") as f:
        for line in f:
            contents = line.strip().split(",")
            name = contents[0].strip()
            email = contents[1].strip()
            try:
                address = ",".join(contents[2:]).strip()
                if address == "":
                    address = None
                participants.append(Participant(name, email, address))
            except IndexError:
                participants.append(Participant(name, email))
    f.close()
    if exceptions:
        _add_exceptions(participants, exceptions)
    return participants


def _add_exceptions(participants, fname):
    exceptions_dict = _generate_exceptions_dict(fname)
    for p in participants:
        if p.name in exceptions_dict:
            exceptions = list()
            for exc in exceptions_dict[p.name]:
                exceptions.append(next(filter(lambda x: x.name == exc, participants)))
            p.exceptions = exceptions


def _generate_exceptions_dict(fname):
    """
    Generates a dictionary where each entry is a dict of the form:
        d[Name] = List of names they can't be matched with

    Parameters
    ----------
    fname: str
        File path to CSV of the form [name, person to exclude_1, ..., person to exclude_n] in the cwd

    Returns
    -------
    dict:
        Key: Name, Value: List of names to exclude

    """
    d = dict()
    with open(fname, "r") as f:
        for line in f:
            contents = line.strip().split(",")
            names_to_exclude = list()
            for i, ex in enumerate(contents):
                if i == 0:
                    name = ex.strip()
                else:
                    names_to_exclude.append(ex.strip())
            d[name] = names_to_exclude
    f.close()
    return d
