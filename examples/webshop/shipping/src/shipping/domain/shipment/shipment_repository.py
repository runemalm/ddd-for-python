from abc import ABCMeta, abstractmethod


class ShipmentRepository(object, metaclass=ABCMeta):
    def __init__(
        self,
    ):
        ShipmentRepository.__init__(self)

    # Operations

    @abstractmethod
    async def get(self, shipment_id):
        pass

    @abstractmethod
    async def save(self, shipment):
        pass

    @abstractmethod
    async def delete(self, shipment):
        pass

    @abstractmethod
    async def get_with_id(
        self,
        shipment_id,
    ):
        pass

    @abstractmethod
    async def get_with_ids(
        self,
        shipment_ids,
    ):
        pass
