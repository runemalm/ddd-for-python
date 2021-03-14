import asyncio
import json

from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import \
    BlobCheckpointStore

from ddd.adapters.event.event_adapter import EventAdapter


class AzureEventAdapter(EventAdapter):

    def __init__(
        self,
        namespace_conn_string,
        checkpoint_store_conn_string,
        blob_container_name,
        topic,
        group,
        log_service,
        service=None,
        listeners=None,
    ):
        super().__init__(
            log_service=log_service,
            service=service,
            listeners=listeners
        )

        self.namespace_conn_string = namespace_conn_string
        self.checkpoint_store_conn_string = checkpoint_store_conn_string
        self.blob_container_name = blob_container_name
        self.topic = topic
        self.group = group

        self.checkpoint_store = None
        self.consumer = None
        self.consumer_task = None

    # Handling

    async def handle(self, message):
        """
        Handle a message.
        """
        message = json.loads(message.body_as_str(encoding='UTF-8'))
        await super().handle(message)

    # Control

    async def start(self):
        await self._create_checkpoint_store()
        await self._create_consumer()
        await self._start_consuming()

    async def stop(self):
        await self._stop_consuming()

    # Azure

    async def _create_checkpoint_store(self):
        self.checkpoint_store = \
            BlobCheckpointStore.from_connection_string(
                self.checkpoint_store_conn_string,
                self.blob_container_name,
            )

    async def _create_consumer(self):
        self.consumer = \
            EventHubConsumerClient.from_connection_string(
                self.namespace_conn_string,
                consumer_group=self.group,
                eventhub_name=self.topic,
                checkpoint_store=self.checkpoint_store,
            )

    async def _start_consuming(self):
        self.consumer_task = \
            asyncio.ensure_future(
                self.consumer.receive(
                    on_event=self._on_event,
                )
            )
        await asyncio.sleep(0.01)

    async def _on_event(self, partition_context, event):
        try:
            await self.handle(event)
        except Exception as e:
            self.log_service.error(
                f"Azure event adapter got exception when "
                f"delegating call to service: '{str(e)}'.",
                exc_info=True,
            )

        # Update the checkpoint so that the program doesn't read the events
        # that it has already read when you run it next time.
        await partition_context.update_checkpoint(event)

    async def _stop_consuming(self):
        self.consumer_task.cancel()
        await self.consumer.close()
