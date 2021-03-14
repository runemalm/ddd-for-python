import arrow

from ddd.tests.action_test_case import ActionTestCase

from webshop.application.iam_application_service import IamApplicationService
from webshop.domain.commands import CreateUserCommand
from webshop.utils.dep_mgr import DependencyManager
from webshop.utils.utils import read_config


class WebshopActionTestCase(ActionTestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName=methodName)

    async def asyncSetUp(self):
        await super().asyncSetUp()

    async def asyncTearDown(self):
        await self.deps.get_customer_repository().delete_all()

        await super().asyncTearDown()

    # Dependencies

    def read_config(self):
        self.config = read_config()

    def _create_deps_manager(self):
        self.deps = DependencyManager(
            config=self.config,
            loop=self.loop,
        )

    def get_service(self):
        if not self.service:
            self.service = \
                WebshopApplicationService(
                    db_service=self.deps.get_db_service(),
                    domain_adapter=self.deps.get_domain_adapter(),
                    domain_publisher=self.deps.get_domain_publisher(),
                    event_repository=self.deps.get_event_repository(),
                    interchange_adapter=self.deps.get_interchange_adapter(),
                    interchange_publisher=
                    self.deps.get_interchange_publisher(),
                    job_service=self.deps.get_job_service(),
                    job_adapter=self.deps.get_job_adapter(),
                    log_service=self.deps.get_log_service(),
                    scheduler_adapter=self.deps.get_scheduler_adapter(),
                    customer_repository=
                    self.deps.get_customer_repository(),
                    max_concurrent_actions=self.config.max_concurrent_actions,
                )

        return self.service

    # Actions

    

    # Helpers

    def _disable_event_listeners(self):
        self._disable_domain_event_listeners()
        self._disable_integration_event_listeners()

    def _disable_domain_event_listeners(self, exclude=None):
        exclude = exclude if exclude is not None else []

        exclude = [
            e.__name__ for e in exclude
        ]

        for listener in self.deps.get_domain_adapter().listeners:
            if listener.listens_to_name not in exclude:
                listener.disable()
            else:
                listener.enable()

    def _disable_integration_event_listeners(self, exclude=None):
        exclude = exclude if exclude is not None else []

        exclude = [
            e.__name__ for e in exclude
        ]

        for listener in self.deps.get_interchange_adapter().listeners:
            if listener.listens_to_name not in exclude:
                listener.disable()
            else:
                listener.enable()
