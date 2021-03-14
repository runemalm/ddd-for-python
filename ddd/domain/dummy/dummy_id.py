from ddd.domain.entity_id import EntityId


class DummyId(EntityId):
    """
    A patient ID.
    """
    def __init__(self, identity):
        super(DummyId, self).__init__(identity=identity)
