class MissingRequiredArgument(Exception):
    """
    Raise this exception if a required argument is not provided
    """

    def __init__(self, msg=None):
        super().__init__(msg)


class FlagConflict(Exception):
    """
    Raise this exception if conflicting flags are provided
    """

    def __init__(self, msg=None):
        super().__init__(msg)
