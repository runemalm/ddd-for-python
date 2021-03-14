from ddd.tests.dummy_action_test_case import DummyActionTestCase
from ddd.domain.dummy.dummy import Dummy
from ddd.repositories.memory.memory_dummy_repository import \
    MemoryDummyRepository


class TestMemoryRepository(DummyActionTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.repository = \
            MemoryDummyRepository(
                log_service=self.deps.get_log_service(),
            )

        Dummy.VERSION = "2"

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
            records,
        )
