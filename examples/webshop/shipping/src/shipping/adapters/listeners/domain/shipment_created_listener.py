from ddd.adapters.event.event_listener import EventListener

from shipping.domain.shipment.shipment_id import ShipmentId
from shipping.domain.shipment.shipment_created import ShipmentCreated


class ShipmentCreatedListener(EventListener):
    def __init__(
        self,
        action,
        service,
        command_creator
    ):
        super().__init__(
            "ShipmentCreated",
            action=action,
            service=service,
            command_creator=command_creator
        )

    def read_event(self):
        super().read_event()

        # Customer ID
        shipment_id = \
            self.reader.entity_id_value(
                'payload.shipment_id', ShipmentId
            )

        # Event
        return ShipmentCreated(
            shipment_id=shipment_id,
            corr_ids=self.corr_ids,
        )
