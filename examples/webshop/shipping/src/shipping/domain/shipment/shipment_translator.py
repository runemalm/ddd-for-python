from ddd.adapters.message_reader import MessageReader

from ddd.utils.utils import str_or_none
from ddd.utils.utils import iso_or_none


class ShipmentTranslator(object):
    def __init__(self, shipment):
        super().__init__()
        self.shipment = shipment

    def to_domain(self):
        return self.to_dict()

    @classmethod
    def from_domain(cls, the_dict):
        from shipping.domain.shipment.shipment import Shipment
        from shipping.domain.shipment.shipment_id import ShipmentId
        from shipping.domain.customer.customer_id import CustomerId

        reader = MessageReader(the_dict)

        # Read
        shipment = Shipment(
            version=reader.string_value('version'),
            shipment_id=reader.entity_id_value('shipment_id', ShipmentId),
            created_at=reader.date_value('created_at'),
            updated_at=reader.date_value('updated_at'),
            customer_id=reader.entity_id_value('customer_id', CustomerId),
        )

        return shipment

    def to_record(self):
        return self.to_dict()

    @classmethod
    def from_record(cls, record):
        the_dict = record['data']
        the_dict['shipment_id'] = record['id']

        return ShipmentTranslator.from_domain(the_dict)

    def to_dict(self):
        return {
            'version': self.shipment.version,
            'shipment_id': str_or_none(self.shipment.shipment_id),
            'created_at': iso_or_none(self.shipment.created_at),
            'updated_at': iso_or_none(self.shipment.updated_at),
            'customer_id': str_or_none(self.shipment.customer_id),
        }
