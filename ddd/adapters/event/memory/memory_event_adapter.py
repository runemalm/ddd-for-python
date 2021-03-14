from ddd.adapters.event.event_adapter import EventAdapter


class MemoryEventAdapter(EventAdapter):

    def __init__(
        self,
        log_service=None,
        service=None,
        listeners=None,
    ):
        super().__init__(
            log_service=log_service,
            service=service,
            listeners=listeners
        )

    # Control

    async def start(self):
        pass

    async def stop(self):
        pass
