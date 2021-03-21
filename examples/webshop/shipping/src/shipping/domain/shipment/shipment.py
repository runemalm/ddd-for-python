from ddd.domain.aggregate import Aggregate


class Shipment(Aggregate):
    """
    A shipment.
    """
    VERSION = "1"

    def __init__(
        self,
        version,
        shipment_id,
        created_at,
        updated_at,
        customer_id,
    ):
        super().__init__(version=version)
        self.shipment_id = shipment_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.customer_id = customer_id
