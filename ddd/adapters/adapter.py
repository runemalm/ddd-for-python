from abc import ABCMeta, abstractmethod


class Adapter(object):
    """
    The adapters base class.

    :param config: The :class:`~ddd.application.config.Config` object.
    :param loop: The event loop.
    :param log_service: The :class:`~ddd.infrastructure.log_service.LogService` object.
    """
    def __init__(
        config, 
        loop, 
        log_service
    ):
        super().__init__()

        # Dependencies
        self.config = config
        self.loop = loop
        self.log_service = log_service

    # Abstract methods (must be implemented by superclasses)

    @abstractmethod
    async def start(self):
        """
        Starts the adapter.
        
        This method is called by the :class:`~ddd.application.application_service.ApplicationService`. When it starts, it starts all the adapters.
        """
        pass

    @abstractmethod
    async def stop(self):
        """
        Stops the adapter.
        
        This method is called by the :class:`~ddd.application.application_service.ApplicationService`. When it stops, it stops all the adapters.
        """
        pass

    # Service

    def set_service(self, service):
        self.service = service
