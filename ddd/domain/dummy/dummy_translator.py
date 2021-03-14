from ddd.adapters.message_reader import MessageReader

from ddd.utils.utils import str_or_none


class DummyTranslator(object):
    def __init__(self, dummy):
        super().__init__()
        self.dummy = dummy

    def to_interchange(self):
        return self.to_dict()

    def to_domain(self):
        return self.to_dict()

    @classmethod
    def from_domain(cls, the_dict):
        from ddd.domain.dummy.dummy import Dummy
        from ddd.domain.dummy.dummy_id import DummyId

        reader = MessageReader(the_dict)

        # Read
        dummy = Dummy(
            version=reader.string_value('version'),
            dummy_id=reader.entity_id_value('dummy_id', DummyId),
            property_added=reader.string_value('property_added'),
        )

        return dummy

    def to_record(self):
        return self.to_dict()

    @classmethod
    def from_record(cls, record):
        the_dict = record['data']
        the_dict['dummy_id'] = record['id']

        return DummyTranslator.from_domain(the_dict)

    def to_dict(self):
        return {
            'version': self.dummy.version,
            'dummy_id': str_or_none(self.dummy.dummy_id),
            'property_added': self.dummy.property_added,
        }
