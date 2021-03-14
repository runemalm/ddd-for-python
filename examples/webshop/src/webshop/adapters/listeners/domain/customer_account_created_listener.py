from ddd.adapters.event.event_listener import EventListener

from webshop.domain.customer_account.customer_account_created import \
    CustomerAccountCreated
from webshop.domain.customer_account.customer_id import CustomerId


class CustomerAccountCreatedListener(EventListener):
    def __init__(
        self,
        action,
        service,
        command_creator
    ):
        super().__init__(
            "CustomerAccountCreated",
            action=action,
            service=service,
            command_creator=command_creator
        )

    def read_event(self):
        super().read_event()

        # Customer ID
        customer_id = \
            self.reader.entity_id_value(
                'payload.customer_id', CustomerId
            )

        # Event
        return CustomerAccountCreated(
            customer_id=customer_id,
            corr_ids=self.corr_ids,
        )
