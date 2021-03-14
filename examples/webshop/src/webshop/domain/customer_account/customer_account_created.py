from ddd.domain.domain_event import DomainEvent


class CustomerAccountCreated(DomainEvent):
    def __init__(self, customer_id, corr_ids):
        super().__init__(
            name="CustomerAccountCreated",
            corr_ids=corr_ids,
        )
        self.customer_id = customer_id

    def get_serialized_payload(self):
        return {
            'customer_id': str(self.customer_id),
        }
