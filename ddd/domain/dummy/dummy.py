from ddd.domain.aggregate import Aggregate


class Dummy(Aggregate):
    """
    A 'dummy' for tests.
    """
    VERSION = "2"

    def __init__(
        self,
        version,
        dummy_id,
        property_added,
    ):
        super().__init__(version=version)
        self.dummy_id = dummy_id
        self.property_added = property_added
