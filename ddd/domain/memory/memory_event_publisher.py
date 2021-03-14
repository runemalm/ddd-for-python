from ddd.domain.event_publisher import EventPublisher


class MemoryEventPublisher(EventPublisher):
    """
    A memory event publisher.
    """
    def __init__(
        self,
        log_service=None,
        keep_flushed_copies=False,
    ):
        super().__init__(
            log_service=log_service,
            keep_flushed_copies=keep_flushed_copies
        )
        self.is_started = False
        self.primary_adapter = None

    # Flush

    async def flush(self, event):
        """
        Actually publishes the event,
        (called after request is done in the 'action' decorator).
        """
        if not self.is_started:
            raise Exception(
                "Can't flush the domain event because "
                "domain publisher isn't started."
            )

        task_id = self._get_loop_task_id()

        if self.primary_adapter:
            for listener in self.primary_adapter.listeners:
                if listener.listens_to(event.name):
                    try:
                        await listener.handle(event.serialize())
                    except Exception as e:
                        self.log_service.error(
                            "Listener failed to handle event '{}', "
                            "exception: {}".
                            format(
                                event.name,
                                str(e),
                            ),
                            exc_info=True,
                        )
        else:
            self.log_service.warning(
                "Couldn't flush events because no primary adapter is set."
            )

        if self.keep_flushed_copies:
            if task_id not in self.flushed:
                self.flushed[task_id] = []

            self.flushed[task_id].append(event)

    # Control

    async def start(self):
        self.is_started = True

    async def stop(self):
        self.is_started = False

    # Setters

    def set_primary_adapter(self, primary_adapter):
        self.primary_adapter = primary_adapter
