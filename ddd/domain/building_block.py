class BuildingBlock(object):
    def __init__(self, version):
        super(BuildingBlock, self).__init__()
        self.version = version

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            a = self.__dict__
            b = other.__dict__
            return a == b
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def equals(self, other, ignore_fields):
        ignore_fields = ignore_fields if ignore_fields is not None else []

        if isinstance(other, self.__class__):

            from ddd.utils.utils import get_for_compare

            a = get_for_compare(self, ignore_fields)
            b = get_for_compare(other, ignore_fields)

            return a == b
        else:
            return False

    def serialize(self, ignore_fields=None):
        """
        Serializes into a dict.
        """
        from ddd.utils.utils import get_for_compare
        return get_for_compare(self, ignore_fields=ignore_fields)
