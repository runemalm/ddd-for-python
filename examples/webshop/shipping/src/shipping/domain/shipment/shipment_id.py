from ddd.domain.entity_id import EntityId


class ShipmentId(EntityId):
    """
    A shipment ID.
    """
    def __init__(self, identity):
        super().__init__(identity=identity)
