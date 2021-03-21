from ddd.domain.domain_event import DomainEvent


class ShipmentCreated(DomainEvent):
    def __init__(self, shipment_id, corr_ids):
        super().__init__(
            name="ShipmentCreated",
            corr_ids=corr_ids,
        )
        self.shipment_id = shipment_id

    def get_serialized_payload(self):
        return {
            'shipment_id': str(self.shipment_id),
        }
