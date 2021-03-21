from abc import ABCMeta, abstractmethod


class CustomerRepository(object, metaclass=ABCMeta):
    def __init__(
        self,
    ):
        CustomerRepository.__init__(self)

    # Operations

    @abstractmethod
    async def get(self, customer_id):
        pass

    @abstractmethod
    async def save(self, customer):
        pass

    @abstractmethod
    async def delete(self, customer):
        pass

    @abstractmethod
    async def get_with_id(
        self,
        customer_id,
    ):
        pass

    @abstractmethod
    async def get_with_ids(
        self,
        customer_ids,
    ):
        pass
