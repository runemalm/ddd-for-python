from ddd.repositories.memory.memory_repository import MemoryRepository

from shipping.domain.shipment.shipment import Shipment
from shipping.domain.shipment.shipment_repository import ShipmentRepository
from shipping.domain.shipment.shipment_translator import ShipmentTranslator


class MemoryShipmentRepository(ShipmentRepository, MemoryRepository):

    def __init__(self, log_service):
        MemoryRepository.__init__(
            self,
            log_service=log_service,
            aggregate_name="shipment",
            aggregate_cls=Shipment,
            translator_cls=ShipmentTranslator,
        )

    async def get(self, shipment_id):
        return await super()._get(shipment_id)

    async def save(self, shipment):
        await super()._save(
            aggregate_id=shipment.shipment_id,
            aggregate=shipment,
        )

    async def delete(self, shipment):
        await self._delete(shipment.shipment_id)

    async def get_with_id(
        self,
        shipment_id,
    ):
        shipments = await self.get_with_ids(shipment_ids=[shipment_id])

        if len(shipments):
            return shipments[0]

        return None

    async def get_with_ids(
        self,
        shipment_ids,
    ):
        records = [
            r for r in self.records.values()
            if r['data']['shipment_id'] in shipment_ids
        ]

        records = self._migrate(records, self.aggregate_cls)

        aggregates = [
            self.aggregate_from_record(record)
            for record in records
        ]

        return aggregates
