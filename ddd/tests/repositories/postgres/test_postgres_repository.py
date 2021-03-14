from ddd.tests.dummy_action_test_case import DummyActionTestCase

from ddd.domain.dummy.dummy import Dummy
from ddd.infrastructure.postgres.postgres_db_service import PostgresDbService
from ddd.repositories.postgres.postgres_dummy_repository import \
    PostgresDummyRepository


class TestPostgresRepository(DummyActionTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.db_service = PostgresDbService(
            dsn=self.config.database.postgres.dsn,
            log_service=self.deps.get_log_service(),
            min_size=20,
            max_size=20,
        )

        self.repository = PostgresDummyRepository(
            config=self.config,
            db_service=self.db_service,
            log_service=self.deps.get_log_service(),
        )

        await self.db_service.start()
        await self.repository.start()

        self.record_v1 = {
            'id': "some-dummy-id-1",
            'data': {
                'version': "1",
            }
        }

        self.record_v2 = {
            'id': "some-dummy-id-2",
            'data': {
                'version': "2",
            }
        }

    async def asyncTearDown(self):
        await self.db_service.stop()
        await self.repository.stop()

    async def test_get_all_records_not_on_latest_version_returns_not_on_latest_version(
        self,
    ):
        # Setup
        await self.repository._save_record(
            aggregate_id=self.record_v1['id'],
            data=self.record_v1['data'],
        )

        await self.repository._save_record(
            aggregate_id=self.record_v2['id'],
            data=self.record_v2['data'],
        )

        Dummy.VERSION = "2"

        # Exercise
        records = await \
            self.repository._get_all_records_not_on_latest_version()

        # Assert
        self.assertEqual(
            [
                self.record_v1,
            ],
            [dict(r) for r in records],
        )
