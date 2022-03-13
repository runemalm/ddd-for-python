from abc import ABCMeta, abstractmethod
from ddd.adapters.adapter import Adapter


class HttpAdapter(Adapter, metaclass=ABCMeta):
    def __init__(self, config, loop, log_service, webhook_callback_token):
        
        super().__init__(
            config=config,
            loop=loop,
            log_service=log_service
        )

        self.webhook_callback_token = webhook_callback_token
