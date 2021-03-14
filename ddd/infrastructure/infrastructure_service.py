from abc import ABCMeta, abstractmethod


class InfrastructureService(object, metaclass=ABCMeta):
    """
    A infrastructure service base class.
    """
    def __init__(self, log_service):
        super().__init__()

        self.log_service = log_service

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass
