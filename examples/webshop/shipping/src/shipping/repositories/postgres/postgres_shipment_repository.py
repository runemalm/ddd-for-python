from ddd.repositories.postgres.postgres_repository import PostgresRepository

from shipping.domain.shipment.shipment import Shipment
from shipping.domain.shipment.shipment_repository import ShipmentRepository
from shipping.domain.shipment.shipment_translator import ShipmentTranslator


class PostgresShipmentRepository(ShipmentRepository, PostgresRepository):
    def __init__(
        self,
        config,
        db_service,
        log_service,
        loop=None,
    ):
        PostgresRepository.__init__(
            self,
            loop=loop,
            db_service=db_service,
            log_service=log_service,
            aggregate_cls=Shipment,
            translator_cls=ShipmentTranslator,
            table_name="shipping_shipments",
            dsn=config.database.postgres.dsn,
        )

    # Operations

    async def get(self, shipment_id):
        return await self._get(aggregate_id=shipment_id)

    async def save(self, shipment):
        await self._save(
            aggregate_id=shipment.shipment_id,
            aggregate=shipment,
        )

    async def delete(self, shipment):
        await self._delete(aggregate_id=shipment.shipment_id)

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
        async with self.db_service.conn_pool.acquire() as conn:
            records = await conn.fetch(
                """SELECT * FROM {}""".
                format(
                    self.table_name
                )
            )

            records = self._migrate(records, Shipment)

            records = \
                self._filter_by_property(
                    records=records,
                    property="shipment_id",
                    values=shipment_ids,
                )

            aggregates = [
                self.aggregate_from_record(record)
                for record in records
            ]

            aggregates.sort(key=lambda r: r.created_at, reverse=True)

            return aggregates
