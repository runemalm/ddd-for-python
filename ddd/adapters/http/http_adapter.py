from abc import ABCMeta, abstractmethod


class HttpAdapter(object, metaclass=ABCMeta):
    def __init__(self, config, loop, log_service, webhook_callback_token):
        super(HttpAdapter, self).__init__()

        self.config = config
        self.loop = loop
        self.log_service = log_service
        self.webhook_callback_token = webhook_callback_token

    # Abstract methods (must be implemented by superclasses)

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass

    # Service

    def set_service(self, service):
        self.service = service
