from ddd.repositories.memory.memory_repository import MemoryRepository

from ddd.domain.dummy.dummy import Dummy
from ddd.domain.dummy.dummy_repository import DummyRepository
from ddd.domain.dummy.dummy_translator import DummyTranslator


class MemoryDummyRepository(DummyRepository, MemoryRepository):

    def __init__(self, log_service):
        MemoryRepository.__init__(
            self,
            log_service=log_service,
            aggregate_name="dummy",
            aggregate_cls=Dummy,
            translator_cls=DummyTranslator,
        )

    async def get(self, dummy_id):
        return await super()._get(dummy_id)

    async def save(self, dummy):
        await super()._save(
            aggregate_id=dummy.dummy_id,
            aggregate=dummy,
        )

    async def delete(self, dummy):
        await self._delete(dummy.dummy_id)
