

class Command(object):
    def __init__(self):
        super(Command, self).__init__()

    # Equality

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
