import asyncio

from abc import ABCMeta

from ddd.adapters.event.azure.azure_event_adapter import AzureEventAdapter
from ddd.adapters.event.kafka.kafka_event_adapter import KafkaEventAdapter
from ddd.adapters.event.memory.memory_event_adapter import MemoryEventAdapter
from ddd.adapters.job.ap_scheduler_adapter import ApSchedulerAdapter
from ddd.adapters.job.job_adapter import JobAdapter
from ddd.adapters.job.memory_scheduler_adapter import MemorySchedulerAdapter
from ddd.domain.azure.azure_event_publisher import AzureEventPublisher
from ddd.domain.kafka.kafka_event_publisher import KafkaEventPublisher
from ddd.domain.memory.memory_event_publisher import MemoryEventPublisher
from ddd.infrastructure.job_service import JobService
from ddd.infrastructure.log_service import LogService
from ddd.infrastructure.memory.memory_db_service import MemoryDbService
from ddd.infrastructure.postgres.postgres_db_service import PostgresDbService
from ddd.repositories.memory.memory_dummy_repository import \
    MemoryDummyRepository
from ddd.repositories.memory.memory_event_repository import \
    MemoryEventRepository
from ddd.repositories.postgres.postgres_dummy_repository import \
    PostgresDummyRepository


class DependencyManager(object, metaclass=ABCMeta):
    """
    A dependency manager used to create & retrieve dependencies.
    """
    def __init__(
        self,
        config,
        loop=None,
    ):
        super().__init__()

        # Vars
        self.config = config
        self.loop = loop if loop else asyncio.get_event_loop()
        self.service = None

        # Dependencies
        self.db_service = None
        self.domain_adapter = None
        self.domain_publisher = None
        self.dummy_repository = None
        self.event_repository = None
        self.interchange_adapter = None
        self.interchange_publisher = None
        self.job_service = None
        self.job_adapter = None
        self.log_service = None
        self.scheduler_adapter = None

    def get_db_service(self):
        if not self.db_service:
            if self.config.database.type == "memory":
                self.db_service = \
                    MemoryDbService(
                        log_service=self.get_log_service(),
                    )
            elif self.config.database.type == "postgres":
                self.db_service = \
                    PostgresDbService(
                        dsn=self.config.database.postgres.dsn,
                        log_service=self.get_log_service(),
                        min_size=20,
                        max_size=20,
                    )
            else:
                raise Exception(
                    f"Db service for type not supported: "
                    f"'{self.config.database.type}'."
                )
        return self.db_service

    def get_domain_adapter(self):
        if not self.domain_adapter:
            if self.config.pubsub.domain.provider == "memory":
                self.domain_adapter = MemoryEventAdapter(
                    log_service=self.get_log_service(),
                )
            elif self.config.pubsub.domain.provider == "kafka":
                self.domain_adapter = KafkaEventAdapter(
                    bootstrap_servers=
                    self.config.pubsub.kafka.bootstrap_servers,
                    topic=self.config.pubsub.domain.topic,
                    group=self.config.pubsub.domain.group,
                    log_service=self.get_log_service(),
                )
            elif self.config.pubsub.domain.provider == "azure":
                self.domain_adapter = AzureEventAdapter(
                    namespace_conn_string=
                    self.config.pubsub.azure.namespace_conn_string,
                    checkpoint_store_conn_string=
                    self.config.pubsub.azure.checkpoint_store_conn_string,
                    blob_container_name=
                    self.config.pubsub.azure.blob_container_name,
                    topic=self.config.pubsub.domain.topic,
                    group=self.config.pubsub.domain.group,
                    log_service=self.get_log_service(),
                )
            else:
                raise Exception(
                    f"Domain adapter for type not supported: "
                    f"'{self.config.pubsub.domain.provider}'."
                )

        return self.domain_adapter

    def get_domain_publisher(self):
        if not self.domain_publisher:
            if self.config.pubsub.domain.provider == "memory":
                self.domain_publisher = MemoryEventPublisher(
                    log_service=self.get_log_service(),
                    keep_flushed_copies=True,
                )
                self.domain_publisher.set_primary_adapter(
                    primary_adapter=self.get_domain_adapter()
                )
            elif self.config.pubsub.domain.provider == "kafka":
                self.domain_publisher = KafkaEventPublisher(
                    bootstrap_servers=
                    self.config.pubsub.kafka.bootstrap_servers,
                    topic=self.config.pubsub.domain.topic,
                    group=self.config.pubsub.domain.group,
                    log_service=self.get_log_service(),
                    keep_flushed_copies=True,
                )
            elif self.config.pubsub.domain.provider == "azure":
                self.domain_publisher = AzureEventPublisher(
                    namespace=self.config.pubsub.azure.namespace,
                    namespace_conn_string=
                    self.config.pubsub.azure.namespace_conn_string,
                    topic=self.config.pubsub.domain.topic,
                    group=self.config.pubsub.domain.group,
                    log_service=self.get_log_service(),
                    keep_flushed_copies=True,
                )
            else:
                raise Exception(
                    f"Domain publisher for type not supported: "
                    f"'{self.config.pubsub.domain.provider}'."
                )
        return self.domain_publisher

    def get_dummy_repository(self):
        if not self.dummy_repository:
            db_type = self.config.database.type
            if db_type == "memory":
                self.dummy_repository = \
                    MemoryDummyRepository(
                        log_service=self.get_log_service(),
                    )
            elif db_type == "postgres":
                self.dummy_repository = \
                    PostgresDummyRepository(
                        config=self.config,
                        db_service=self.get_db_service(),
                        log_service=self.get_log_service(),
                    )
            else:
                raise Exception("Unsupported db type: '{db_type}'")
        return self.dummy_repository

    def get_event_repository(self):
        if not self.event_repository:
            self.event_repository = MemoryEventRepository()
        return self.event_repository

    def get_interchange_adapter(self):
        if not self.interchange_adapter:

            if self.config.pubsub.interchange.provider == "memory":
                self.interchange_adapter = MemoryEventAdapter(
                    log_service=self.get_log_service(),
                )
            elif self.config.pubsub.interchange.provider == "kafka":
                self.interchange_adapter = KafkaEventAdapter(
                    bootstrap_servers=
                    self.config.pubsub.kafka.bootstrap_servers,
                    topic=self.config.pubsub.interchange.topic,
                    group=self.config.pubsub.interchange.group,
                    log_service=self.get_log_service(),
                )
            elif self.config.pubsub.interchange.provider == "azure":
                self.interchange_adapter = AzureEventAdapter(
                    namespace_conn_string=
                    self.config.pubsub.azure.namespace_conn_string,
                    checkpoint_store_conn_string=
                    self.config.pubsub.azure.checkpoint_store_conn_string,
                    blob_container_name=
                    self.config.pubsub.azure.blob_container_name,
                    topic=self.config.pubsub.interchange.topic,
                    group=self.config.pubsub.interchange.group,
                    log_service=self.get_log_service(),
                )
            else:
                raise Exception(
                    f"Interchange adapter for type not supported: "
                    f"'{self.config.pubsub.interchange.provider}'."
                )

        return self.interchange_adapter

    def get_interchange_publisher(self):
        if not self.interchange_publisher:
            if self.config.pubsub.interchange.provider == "memory":
                self.interchange_publisher = MemoryEventPublisher(
                    log_service=self.get_log_service(),
                    keep_flushed_copies=True,
                )
                self.interchange_publisher.set_primary_adapter(
                    primary_adapter=self.get_interchange_adapter()
                )
            elif self.config.pubsub.interchange.provider == "kafka":
                self.interchange_publisher = KafkaEventPublisher(
                    bootstrap_servers=
                    self.config.pubsub.kafka.bootstrap_servers,
                    topic=self.config.pubsub.interchange.topic,
                    group=self.config.pubsub.interchange.group,
                    log_service=self.get_log_service(),
                    keep_flushed_copies=True,
                )
            elif self.config.pubsub.interchange.provider == "azure":
                self.interchange_publisher = AzureEventPublisher(
                    namespace=self.config.pubsub.azure.namespace,
                    namespace_conn_string=
                    self.config.pubsub.azure.namespace_conn_string,
                    topic=self.config.pubsub.interchange.topic,
                    group=self.config.pubsub.interchange.group,
                    log_service=self.get_log_service(),
                    keep_flushed_copies=True,
                )
            else:
                raise Exception(
                    f"Interchange publisher for type not supported: "
                    f"'{self.config.pubsub.interchange.provider}'."
                )
        return self.interchange_publisher

    def get_job_adapter(self):
        if not self.job_adapter:
            self.job_adapter = \
                JobAdapter(
                    log_service=self.get_log_service(),
                    token=self.config.auth.full_access_token,
                )
        return self.job_adapter

    def get_job_service(self):
        if not self.job_service:
            self.job_service = \
                JobService(
                    scheduler_adapter=self.get_scheduler_adapter(),
                    log_service=self.log_service,
                )
        return self.job_service

    def get_log_service(self):
        if not self.log_service:
            slack_config = self.config.slack
            slack_config.token = self.config.slack.token
            slack_config.bot_username = "Log Service (ddd-for-python)"

            kibana_config = self.config.log.kibana
            kibana_config.source = "Log Service (ddd-for-python)"

            self.log_service = \
                LogService(
                    kibana_config=kibana_config,
                    slack_config=slack_config,
                )

        return self.log_service

    def get_scheduler_adapter(self):
        if not self.scheduler_adapter:
            if self.config.jobs.scheduler.type == "apscheduler":
                self.scheduler_adapter = ApSchedulerAdapter(
                    dsn=self.config.jobs.scheduler.dsn,
                    exec_func=self.get_job_adapter().run_job,
                    log_service=self.get_log_service(),
                )
            elif self.config.jobs.scheduler.type == "memory":
                self.scheduler_adapter = MemorySchedulerAdapter(
                    exec_func=self.get_job_adapter().run_job,
                    log_service=self.get_log_service(),
                )
            else:
                raise Exception(
                    f"Scheduler adapter for type not supported: "
                    f"'{self.config.jobs.scheduler.type}'."
                )
        return self.scheduler_adapter

    def get_service(self):
        return self.service

    def set_service(self, service):
        self.service = service
        self.wire_together()

    def wire_together(self):
        self.get_domain_adapter().set_service(self.service)
        self.get_interchange_adapter().set_service(self.service)
        self.get_job_adapter().set_service(self.service)
