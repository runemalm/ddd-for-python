class DomainException(Exception):
    """
    A domain exception.
    """
    def __init__(self, errors):
        super(DomainException, self).__init__()
        self.errors = errors

    def __str__(self):
        return ",".join([e['message'] for e in self.errors])
