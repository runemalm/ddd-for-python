from ddd.adapters.message_reader import MessageReader

from ddd.utils.utils import str_or_none
from ddd.utils.utils import iso_or_none


class CustomerTranslator(object):
    def __init__(self, customer):
        super().__init__()
        self.customer = customer

    def to_domain(self):
        return self.to_dict()

    @classmethod
    def from_domain(cls, the_dict):
        from shipping.domain.customer.customer import Customer
        from shipping.domain.customer.customer_id import CustomerId

        reader = MessageReader(the_dict)

        # Read
        customer = Customer(
            version=reader.string_value('version'),
            customer_id=reader.entity_id_value('customer_id', CustomerId),
            created_at=reader.date_value('created_at'),
            updated_at=reader.date_value('updated_at'),
            email=reader.string_value('email'),
            first_name=reader.string_value('first_name'),
            last_name=reader.string_value('last_name'),
        )

        return customer

    def to_record(self):
        return self.to_dict()

    @classmethod
    def from_record(cls, record):
        the_dict = record['data']
        the_dict['customer_id'] = record['id']

        return CustomerTranslator.from_domain(the_dict)

    def to_dict(self):
        return {
            'version': self.customer.version,
            'user_id': str_or_none(self.customer.customer_id),
            'created_at': iso_or_none(self.customer.created_at),
            'updated_at': iso_or_none(self.customer.updated_at),
            'email': self.customer.email,
            'first_name': self.customer.first_name,
            'last_name': self.customer.last_name,
        }
