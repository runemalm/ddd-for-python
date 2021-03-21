from unittest import skip

from ddd.tests.dummy_action_test_case import DummyActionTestCase

from ddd.adapters.event.memory.memory_event_adapter import MemoryEventAdapter

from shipping.adapters.listeners.domain.shipment_created_listener \
    import ShipmentCreatedListener
from shipping.application.shipping_application_service import \
    ShippingApplicationService
from shipping.domain.commands import SendTrackingEmailCommand


class TestEventAdapter(DummyActionTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.adapter = MemoryEventAdapter()

    async def test_assigns_service_to_listeners_when_setting_service(
        self,
    ):
        # Setup
        listener = \
            ShipmentCreatedListener(
                action="send_tracking_email",
                service=None,
                command_creator=lambda event:
                SendTrackingEmailCommand(
                    shipment_id=event.shipment_id,
                    token=None,
                )
            )

        self.adapter.set_listeners([
            listener
        ])

        service = ShippingApplicationService(
            customer_repository=None,
            db_service=None,
            domain_adapter=None,
            domain_publisher=None,
            event_repository=None,
            interchange_adapter=None,
            interchange_publisher=None,
            job_adapter=None,
            job_service=None,
            log_service=None,
            scheduler_adapter=None,
            shipment_repository=None,
            max_concurrent_actions=10,
            loop=None,
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
