from ddd.utils.dep_mgr import DependencyManager as BaseDependencyManager
from ddd.infrastructure.log_service import LogService

from shipping.repositories.memory.memory_customer_repository import \
    MemoryCustomerRepository
from shipping.repositories.postgres.postgres_customer_repository import \
    PostgresCustomerRepository
from shipping.repositories.memory.memory_shipment_repository import \
    MemoryShipmentRepository
from shipping.repositories.postgres.postgres_shipment_repository import \
    PostgresShipmentRepository


class DependencyManager(BaseDependencyManager):
    """
    The dependency manager for shipping context.

    All base dependencies are in super class.

    In this class, we add deps specific to this context.
    """
    def __init__(
        self,
        config,
        loop=None,
    ):
        super().__init__(
            config=config,
            loop=loop,
        )
        self.customer_repository = None
        self.shipment_repository = None

    def get_customer_repository(self):
        if not self.customer_repository:
            db_type = self.config.database.type
            if db_type == "memory":
                self.customer_repository = \
                    MemoryCustomerRepository(
                        log_service=self.get_log_service(),
                    )
            elif db_type == "postgres":
                self.customer_repository = \
                    PostgresCustomerRepository(
                        config=self.config,
                        db_service=self.get_db_service(),
                        log_service=self.get_log_service(),
                    )
            else:
                raise Exception("Unsupported db type: '{db_type}'")

        return self.customer_repository

    def get_domain_adapter(self):
        """
        We override from super class so that we can
        set the listeners here.
        """
        if not self.domain_adapter:
            domain_adapter = super().get_domain_adapter()

            domain_adapter.set_listeners([

            ])
        return self.domain_adapter

    def get_interchange_adapter(self):
        """
        We override from super class so that we can
        set the listeners here.
        """
        if not self.interchange_adapter:

            interchange_adapter = super().get_interchange_adapter()

            interchange_adapter.set_listeners([

            ])

        return self.interchange_adapter

    def get_log_service(self):
        """
        We override from super class so that we can
        change the logger source name.
        """
        if not self.log_service:
            slack_config = self.config.slack
            slack_config.token = self.config.slack.token
            slack_config.bot_username = f"Webshop"

            kibana_config = self.config.log.kibana
            kibana_config.source = f"Webshop"

            self.log_service = \
                LogService(
                    kibana_config=kibana_config,
                    slack_config=slack_config,
                )
        return self.log_service

    def get_shipment_repository(self):
        if not self.shipment_repository:
            db_type = self.config.database.type
            if db_type == "memory":
                self.shipment_repository = \
                    MemoryShipmentRepository(
                        log_service=self.get_log_service(),
                    )
            elif db_type == "postgres":
                self.shipment_repository = \
                    PostgresShipmentRepository(
                        config=self.config,
                        db_service=self.get_db_service(),
                        log_service=self.get_log_service(),
                    )
            else:
                raise Exception("Unsupported db type: '{db_type}'")

        return self.shipment_repository
