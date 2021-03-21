from ddd.repositories.memory.memory_repository import MemoryRepository

from shipping.domain.customer.customer import Customer
from shipping.domain.customer.customer_repository import CustomerRepository
from shipping.domain.customer.customer_translator import CustomerTranslator


class MemoryCustomerRepository(CustomerRepository, MemoryRepository):

    def __init__(self, log_service):
        MemoryRepository.__init__(
            self,
            log_service=log_service,
            aggregate_name="customer",
            aggregate_cls=Customer,
            translator_cls=CustomerTranslator,
        )

    async def get(self, customer_id):
        return await super()._get(customer_id)

    async def save(self, customer):
        await super()._save(
            aggregate_id=customer.customer_id,
            aggregate=customer,
        )

    async def delete(self, customer):
        await self._delete(customer.customer_id)

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
        records = [
            r for r in self.records.values()
            if r['data']['customer_id'] in customer_ids
        ]

        records = self._migrate(records, self.aggregate_cls)

        aggregates = [
            self.aggregate_from_record(record)
            for record in records
        ]

        return aggregates
