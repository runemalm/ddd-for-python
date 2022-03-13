from ddd.domain.entity_id import EntityId


class CustomerId(EntityId):
    """
    A customer ID.
    """
    def __init__(self, identity):
        super().__init__(identity=identity)
