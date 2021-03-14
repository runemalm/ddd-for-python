from ddd.tests.dummy_action_test_case import DummyActionTestCase
from ddd.utils.tasks.migrate_models import Task as MigrateModelsTask
from ddd.domain.dummy.dummy import Dummy


class TestMigrateModels(DummyActionTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()

    async def test_records_migrated_to_latest_version_when_running(
        self,
    ):
        # Setup
        Dummy.VERSION = "2"

        aggregate_id = "some-dummy-id"

        data = {
            'version': "1",
            'dummy_id': aggregate_id,
        }

        repository = self.deps.get_dummy_repository()

        await repository._save_record(
            aggregate_id=aggregate_id,
            data=data,
        )

        command = \
            MigrateModelsTask(
                config=self.config,
                deps_mgr=self.deps,
                args_str="",
            )

        # Exercise
        await command._run()

        record = \
            await repository._get_record(
                aggregate_id=aggregate_id,
            )

        # Assert
        self.assertEqual(
            {
                'id': aggregate_id,
                'data': {
                    'version': "2",
                    'dummy_id': aggregate_id,
                    'property_added': 'in_version_2',
                },
            },
            dict(record),
        )
