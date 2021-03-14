import asyncio

from abc import ABCMeta, abstractmethod

from ddd.application.domain_registry import DomainRegistry


class EventPublisher(object, metaclass=ABCMeta):
    """
    The event publisher interface.
    """
    def __init__(self, log_service=None, keep_flushed_copies=False):

        self.log_service = \
            log_service \
            if log_service \
            else DomainRegistry.get_instance().log_service

        self.keep_flushed_copies = keep_flushed_copies

        self.published = {}
        self.flushed = {}

    # To override

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass

    @abstractmethod
    async def flush(self, event):
        """
        Flush (actually publish) the events.
        """
        pass

    # Methods

    async def publish(self, event):
        """
        Publish an event.
        """
        task_id = self._get_loop_task_id()

        if task_id not in self.published:
            self.published[task_id] = []

        # Log
        extra = {}

        self.log_service.debug(
            f"Publishing event: {event.name}",
            extra=extra,
        )

        self.published[task_id].append(event)

    def get_published(self):
        task_id = self._get_loop_task_id()

        if task_id in self.published:
            return self.published[task_id]

        return []

    def clear_published(self):
        task_id = self._get_loop_task_id()

        if task_id in self.published:
            self.published[task_id] = []

    def has_flushed(self, event, ignore_fields=None):
        ignore_fields = ignore_fields if ignore_fields is not None else []

        for task_id in self.flushed:
            for e in self.flushed[task_id]:
                if e.equals(event, ignore_fields=ignore_fields):
                    return True
        return False

    # Helpers

    def _get_loop_task_id(self):
        """
        Get currently executing asyncio event loop task.
        """
        if hasattr(asyncio, "current_task"):  # python >= 3.7
            task_id = id(asyncio.current_task())
        elif hasattr(asyncio.Task, "current_task"):  # python >= 3.6 < 3.7
            task_id = id(asyncio.Task.current_task())
        else:
            raise Exception(
                "Couldn't get currently running task on asyncio event loop. "
                "The version of python you're using isn't supported by "
                "this library."
            )
