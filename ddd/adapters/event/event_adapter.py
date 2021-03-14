from abc import ABCMeta, abstractmethod

from ddd.application.domain_registry import DomainRegistry


class EventAdapter(object, metaclass=ABCMeta):

    def __init__(self, log_service=None, service=None, listeners=None):
        super().__init__()

        self.log_service = \
            log_service \
            if log_service \
            else DomainRegistry.get_instance().log_service

        self.service = service
        self.listeners = [] if listeners is None else []
        self._assign_service_to_listeners()

    # Service

    def set_service(self, service):
        self.service = service
        self._assign_service_to_listeners()

    # Listeners

    def set_listeners(self, listeners):
        self.listeners = listeners
        self._assign_service_to_listeners()

    # Handling

    async def handle(self, message):
        for listener in self.listeners:
            if listener.listens_to(message['name']):
                await listener.handle(message)

    # Control

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass

    # Helpers

    def _assign_service_to_listeners(self):
        for listener in self.listeners:
            listener.service = self.service
