from unittest import skip

from ddd.tests.dummy_action_test_case import DummyActionTestCase

from ddd.adapters.event.memory.memory_event_adapter import MemoryEventAdapter

from webshop.adapters.listeners.domain.customer_account_created_listener \
    import CustomerAccountCreatedListener
from webshop.application.webshop_application_service import \
    WebshopApplicationService
from webshop.domain.commands import SendWelcomeEmailCommand


class TestEventAdapter(DummyActionTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.adapter = MemoryEventAdapter()

    async def test_assigns_service_to_listeners_when_setting_service(
        self,
    ):
        # Setup
        listener = \
            CustomerAccountCreatedListener(
                action="send_welcome_email",
                service=None,
                command_creator=lambda event:
                SendWelcomeEmailCommand(
                    customer_id=event.customer_id,
                    token=None,
                )
            )

        self.adapter.set_listeners([
            listener
        ])

        service = WebshopApplicationService(
            db_service=None,
            domain_adapter=None,
            domain_publisher=None,
            event_repository=None,
            interchange_adapter=None,
            interchange_publisher=None,
            job_service=None,
            job_adapter=None,
            log_service=None,
            scheduler_adapter=None,
            customer_repository=None,
            max_concurrent_actions=10,
        )

        # Exercise
        self.adapter.set_service(service)

        # Assert
        for listener in self.adapter.listeners:
            self.assertEqual(service, listener.service)

    @skip
    async def test_assigns_service_to_listeners_when_setting_listeners(
        self,
    ):
        raise NotImplementedError()

    @skip
    async def test_delegates_event_to_listeners(
        self,
    ):
        raise NotImplementedError()
