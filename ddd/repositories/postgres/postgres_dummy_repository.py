from ddd.repositories.postgres.postgres_repository import PostgresRepository

from ddd.domain.dummy.dummy import Dummy
from ddd.domain.dummy.dummy_repository import DummyRepository
from ddd.domain.dummy.dummy_translator import DummyTranslator


class PostgresDummyRepository(DummyRepository, PostgresRepository):
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
            aggregate_cls=Dummy,
            translator_cls=DummyTranslator,
            table_name="ddd_dummies",
            dsn=config.database.postgres.dsn,
        )

    # Operations

    async def get(self, dummy_id):
        return await self._get(aggregate_id=dummy_id)

    async def save(self, dummy):
        await self._save(
            aggregate_id=dummy.dummy_id,
            aggregate=dummy,
        )

    async def delete(self, dummy):
        await self._delete(aggregate_id=dummy.dummy_id)
