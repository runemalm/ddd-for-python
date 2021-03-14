import asyncio
import json

from aiokafka import AIOKafkaProducer

from ddd.domain.event_publisher import EventPublisher


class KafkaEventPublisher(EventPublisher):
    """
    A kafka event publisher.
    """
    def __init__(
        self,
        bootstrap_servers,
        topic,
        group,
        log_service,
        keep_flushed_copies=False,
    ):
        super().__init__(
            log_service=log_service,
            keep_flushed_copies=keep_flushed_copies
        )
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group = group

        self.is_started = False

    # Flush

    async def flush(self, event):
        """
        Actually publishes the event,
        (called after request is done in the 'action' decorator).
        """
        task_id = self._get_loop_task_id()

        prefix = "[ -------- ]"

        if not self.producer:
            raise Exception(
                (
                    "Kafka event publisher couldn't publish because "
                    "producer has not been created."
                )
            )

        await self.producer.send_and_wait(
            self.topic,
            json.dumps(event.serialize()).encode()
        )

        if self.keep_flushed_copies:
            if task_id not in self.flushed:
                self.flushed[task_id] = []

            self.flushed[task_id].append(event)

    # Control

    async def start(self):
        await self.create_producer()
        await self.connect(
            retry_backoff=6,
            max_retries=3,
        )

    async def stop(self):
        if not self.producer:
            self.log_service.warning(
                (
                    "Kafka event publisher was instructed to stop "
                    "but it doesn't seem to be started (no producer)."
                )
            )
        else:
            await self.disconnect()

    # Connect

    async def connect(self, retry_backoff=6, max_retries=12):
        created = False
        error = None
        retry_backoff = retry_backoff
        retries = 0
        max_retries = max_retries

        while (not created) and retries < max_retries:
            try:
                await self.producer.start()
                self.producer_connected = True
                created = True

            except Exception as e:
                self.log_service.error(
                    (
                        "{} failed to connect to: {} "
                        "(retrying in {} secs..), exception: {}"
                    ).
                    format(
                        "Kafka Event Publisher",
                        self.bootstrap_servers,
                        retry_backoff,
                        str(e)
                    )
                )
                error = str(e)
                retries += 1
                await asyncio.sleep(retry_backoff)

        if not created:
            raise Exception(
                (
                    "{} failed to connect to: {} "
                    "after {} retries, error: {}."
                ).
                format(
                    "Kafka Event Publisher",
                    self.bootstrap_servers,
                    retries,
                    error
                )
            )

        await self.wait_for_connect()

        self.log_service.debug(
            "Kafka event publisher connected to {} @ {}".
            format(
                self.topic,
                self.bootstrap_servers
            )
        )

    async def disconnect(self):
        await self.producer.stop()
        self.producer_connected = False

    async def wait_for_connect(self, timeout=60):
        waited = 0
        while not self.producer_connected:
            await asyncio.sleep(1)
            waited = waited + 1
            if waited > timeout:
                raise Exception(
                    "Couldn't connect to kafka, timed out after {} secs".
                    format(
                        timeout
                    )
                )

    # Publishing

    async def create_producer(self):
        self.producer = AIOKafkaProducer(
            loop=asyncio.get_event_loop(),
            bootstrap_servers=self.bootstrap_servers
        )
