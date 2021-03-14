from abc import ABCMeta, abstractmethod


class DummyRepository(object, metaclass=ABCMeta):
    def __init__(
        self,
    ):
        DummyRepository.__init__(self)

    # Operations



    # Migration

    def _migrate_v1_to_v2(self, record):
        """
        Add: 'property_added'
        """
        record['data']['property_added'] = "in_version_2"

        return record
