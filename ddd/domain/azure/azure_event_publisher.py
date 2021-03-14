import asyncio
import json

from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

from ddd.domain.event_publisher import EventPublisher


class AzureEventPublisher(EventPublisher):
    """
    A azure event publisher.
    """
    def __init__(
        self,
        namespace,
        namespace_conn_string,
        topic,
        group,
        log_service,
        keep_flushed_copies=False,
    ):
        super().__init__(
            log_service=log_service,
            keep_flushed_copies=keep_flushed_copies
        )
        self.namespace = namespace
        self.namespace_conn_string = namespace_conn_string
        self.topic = topic
        self.group = group

    # Flush

    async def flush(self, event):
        """
        Actually publishes the event,
        (called after request is done in the 'action' decorator).
        """
        task_id = self._get_loop_task_id()

        if not self.producer:
            raise Exception(
                (
                    "Azure event publisher couldn't publish because "
                    "producer has not been created."
                )
            )

        # Serialize
        try:
            json_data = json.dumps(event.serialize()).encode()
        except TypeError:
            self.log_service.error(
                "Failed to flush an event! The event couldn't be serialized, "
                "(check log details for event data).",
                extra={
                    'event_data': event.serialize(),
                }
            )
            raise

        # Without specifying partition_id or partition_key
        # the events will be distributed to available partitions via
        # round-robin.
        event_data_batch = await self.producer.create_batch()

        event_data_batch.add(
            EventData(
                json_data
            )
        )
        await self.producer.send_batch(event_data_batch)

        if self.keep_flushed_copies:
            if task_id not in self.flushed:
                self.flushed[task_id] = []

            self.flushed[task_id].append(event)

    # Control

    async def start(self):
        await self.create_producer()

    async def stop(self):
        if not self.producer:
            self.log_service.warning(
                (
                    "Azure event publisher was instructed to stop "
                    "but it doesn't seem to be started (no producer)."
                )
            )
        else:
            await self.producer.close()

    # Publishing

    async def create_producer(self):
        self.producer = \
            EventHubProducerClient.from_connection_string(
                conn_str=self.namespace_conn_string,
                eventhub_name=self.topic,
            )
        await asyncio.sleep(0.01)
