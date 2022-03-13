from ddd.repositories.postgres.postgres_repository import PostgresRepository

from shipping.domain.customer.customer import Customer
from shipping.domain.customer.customer_repository import CustomerRepository
from shipping.domain.customer.customer_translator import CustomerTranslator


class PostgresCustomerRepository(CustomerRepository, PostgresRepository):
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
            aggregate_cls=Customer,
            translator_cls=CustomerTranslator,
            table_name="webshop_customers",
            dsn=config.database.postgres.dsn,
        )

    # Operations

    async def get(self, customer_id):
        return await self._get(aggregate_id=customer_id)

    async def save(self, customer):
        await self._save(
            aggregate_id=customer.customer_id,
            aggregate=customer,
        )

    async def delete(self, customer):
        await self._delete(aggregate_id=customer.customer_id)

    async def get_with_id(
        self,
        customer_id,
    ):
        customers = await self.get_with_ids(customer_ids=[customer_id])

        if len(customers):
            return customers[0]

        return None

    async def get_with_ids(
        self,
        customer_ids,
    ):
        async with self.db_service.conn_pool.acquire() as conn:
            records = await conn.fetch(
                """SELECT * FROM {}""".
                format(
                    self.table_name
                )
            )

            records = self._migrate(records, Customer)

            records = \
                self._filter_by_property(
                    records=records,
                    property="customer_id",
                    values=customer_ids,
                )

            aggregates = [
                self.aggregate_from_record(record)
                for record in records
            ]

            aggregates.sort(key=lambda r: r.created_at, reverse=True)

            return aggregates
