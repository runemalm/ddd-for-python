from ddd.utils.dep_mgr import DependencyManager as BaseDependencyManager
from ddd.infrastructure.log_service import LogService

from webshop.repositories.memory.memory_customer_repository import MemoryCustomerRepository
from webshop.repositories.postgres.postgres_customer_repository import \
    PostgresCustomerRepository


class DependencyManager(BaseDependencyManager):

    def __init__(
        self,
        config,
        loop=None,
    ):
        super().__init__(
            config=config,
            loop=loop,
        )
        self.audit_service = None
        self.domain_adapter = None
        self.group_repository = None
        self.http_adapter = None
        self.interchange_adapter = None
        self.legacy_adapter = None
        self.permission_repository = None
        self.role_repository = None
        self.user_repository = None

    def get_domain_adapter(self):
        if not self.domain_adapter:
            domain_adapter = super().get_domain_adapter()

            domain_adapter.set_listeners([

            ])
        return self.domain_adapter

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

    # def get_http_adapter(self):
    #     if not self.http_adapter:
    #         self.http_adapter = \
    #             HttpIamAdapter(
    #                 config=self.config,
    #                 loop=None,
    #                 logtest_create_user_service=self.get_log_service(),
    #                 webhook_callback_token=
    #                 self.config.auth.full_access_token
    #             )
    #     return self.http_adapter

    def get_interchange_adapter(self):
        if not self.interchange_adapter:

            interchange_adapter = super().get_interchange_adapter()

            interchange_adapter.set_listeners([

            ])

        return self.interchange_adapter

    def get_log_service(self):
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

    def wire_together(self):
        """
        Assign references between the deps.
        """
        super().wire_together()

        # self.get_http_adapter().set_service(self.service)
