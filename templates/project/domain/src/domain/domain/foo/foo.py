from ddd.domain.aggregate import Aggregate


class Customer(Aggregate):
    """
    A customer.
    """
    VERSION = "1"

    def __init__(
        self,
        version,
        customer_id,
        created_at,
        updated_at,
        email,
        first_name,
        last_name,
    ):
        super().__init__(version=version)
        self.customer_id = customer_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
