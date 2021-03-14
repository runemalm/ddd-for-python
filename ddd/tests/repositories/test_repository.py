from addict import Dict

from unittest.mock import MagicMock

from ddd.domain.dummy.dummy import Dummy
from ddd.repositories.postgres.postgres_dummy_repository import \
    PostgresDummyRepository

from ddd.tests.dummy_action_test_case import DummyActionTestCase


class TestRepository(DummyActionTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.repository = \
            PostgresDummyRepository(
                config=Dict({'database': {'dsn': "some-dsn"}}),
                db_service=None,
                log_service=self.deps.get_log_service(),
            )

        self.record_v1 = {
            'id': "some-dummy-id",
            'data': {
                'version': "1",
            }
        }

        self.record_v2 = {
            'id': "some-dummy-id",
            'data': {
                'version': "1",
                'second': "value",
            }
        }

        self.record_v3 = {
            'id': "some-dummy-id",
            'data': {
                'version': "1",
                'second': "value",
                'third': "value",
            }
        }

    async def test_get_versions_to_migrate_to_returns_unmigrated_versions_when_not_on_latest_version(
        self,
    ):
        # Setup
        Dummy.VERSION = "3"

        # Exercise
        versions = \
            self.repository._get_versions_to_migrate_to(
                record=self.record_v1,
                cls=Dummy,
            )

        # Assert
        self.assertEqual(
            range(2, 3),
            versions,
        )

    async def test_get_versions_to_migrate_to_returns_no_range_when_on_latest_version(
        self,
    ):
        # Setup
        Dummy.VERSION = "1"

        # Exercise
        versions = \
            self.repository._get_versions_to_migrate_to(
                record=self.record_v1,
                cls=Dummy,
            )

        # Assert
        self.assertEqual(
            range(0, 0),
            versions,
        )

    async def test_migrate_calls_all_migration_funcs(
        self,
    ):
        # Setup
        Dummy.VERSION = "3"

        # ..mock
        mock_migrate_v1_to_v2 = MagicMock(
            return_value=self.record_v2,
        )

        mock_migrate_v2_to_v3 = MagicMock(
            return_value=self.record_v3,
        )

        self.repository._migrate_v1_to_v2 = mock_migrate_v1_to_v2
        self.repository._migrate_v2_to_v3 = mock_migrate_v2_to_v3

        # Exercise
        self.repository._migrate(
            records=[self.record_v1],
            cls=Dummy,
        )

        # Assert
        mock_migrate_v1_to_v2.assert_called_with(
            record=self.record_v1,
        )

        mock_migrate_v2_to_v3.assert_called_with(
            record=self.record_v2,
        )
