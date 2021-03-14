import asyncio
import json

from aiokafka import AIOKafkaConsumer

from ddd.adapters.event.event_adapter import EventAdapter


class KafkaEventAdapter(EventAdapter):

    def __init__(
        self,
        bootstrap_servers,
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

        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group = group

        self.consumer_connected = False
        self.consumer_stopped = False
        self.consuming = False

    # Handling

    async def handle(self, message):
        """
        Handle a message.
        """
        message = json.loads(message.value)
        await super().handle(message)

    # Control

    async def start(self):
        await self._create_consumer()
        await self._connect()
        await self._start_consuming()

    async def stop(self):
        await self._stop_consuming()
        await self._disconnect()

    async def _create_consumer(self):
        self.consumer = \
            AIOKafkaConsumer(
                self.topic,
                loop=asyncio.get_event_loop(),
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group,
                enable_auto_commit=False
            )

    async def _connect(self):
        created = False
        error = None
        backoff = 6
        retries = 0
        max_retries = 3

        while (not created) and (retries < max_retries):
            try:
                await self.consumer.start()
                self.consumer_connected = True
                created = True

            except Exception as e:
                self.log_service.error(
                    (
                        "{} failed to connect to: {} "
                        "(retrying in {} secs..), exception: {}"
                    ).format(
                        "Kafka Event Adapter",
                        self.bootstrap_servers,
                        backoff,
                        str(e)
                    )
                )
                error = str(e)
                retries += 1
                await asyncio.sleep(backoff)

        if not created:
            raise Exception(
                (
                    "{} failed to connect to: {} "
                    "after {} retries, error: {}."
                ).format(
                    "Kafka Event Adapter",
                    self.bootstrap_servers,
                    retries,
                    error
                )
            )

        await self._wait_for_connect()

        self.log_service.debug(
            "Kafka event adapter listens on {} @ {}, (group: {})".
                format(
                self.topic,
                self.bootstrap_servers,
                self.group
            )
        )

    async def _wait_for_connect(self, timeout=60):
        waited = 0
        while not self.consumer_connected:
            await asyncio.sleep(1)
            waited = waited + 1
            if waited > timeout:
                raise Exception(
                    "Couldn't connect to kafka, timed out after {} secs".
                    format(
                        timeout
                    )
                )

    async def _start_consuming(self):
        # Schedule in a new task on the event loop to prevent blocking
        asyncio.get_event_loop().create_task(
            self._consume()
        )

    async def _consume(self):
        self.consuming = True

        while not self.consumer_stopped:
            try:
                message = await asyncio.wait_for(
                    self.consumer.__anext__(),
                    timeout=3
                )
                try:
                    await self.handle(message)
                except Exception as e:
                    self.log_service.error(
                        f"Kafka Event Adapter got exception when "
                        f"delegating call to service: '{str(e)}'.",
                        exc_info=True,
                    )
                await self.consumer.commit()
            except asyncio.TimeoutError:
                pass

        self.consuming = False

    async def _stop_consuming(self):
        self.consumer_stopped = True
        await self.wait_for_consumption_to_stop()

    async def wait_for_consumption_to_stop(self, timeout=60):
        waited = 0
        while self.consuming:
            await asyncio.sleep(1)
            waited = waited + 1
            if waited > timeout:
                raise Exception(
                    (
                        "Failed waiting for consumption to stop, "
                        "timed out after {} secs"
                    ).format(
                        timeout
                    )
                )

    async def _disconnect(self):
        # Will leave consumer group; perform autocommit if enabled.
        await self.consumer.stop()
        self.consumer_connected = False

    async def _wait_for_disconnect(self, timeout=60):
        waited = 0
        while self.consumer_connected:
            await asyncio.sleep(1)
            waited = waited + 1
            if waited > timeout:
                raise Exception(
                    (
                        "Couldn't disconnect from kafka, timed out "
                        "after {} secs"
                    ).format(
                        timeout
                    )
                )
