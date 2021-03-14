from ddd.application.application_service import ApplicationService
from ddd.application.action import action


class DummyApplicationService(ApplicationService):
    """
    This is the dummy context's application service.
    """
    def __init__(
        self,
        db_service,
        domain_adapter,
        domain_publisher,
        event_repository,
        interchange_adapter,
        interchange_publisher,
        job_service,
        job_adapter,
        log_service,
        scheduler_adapter,
        dummy_repository,
        max_concurrent_actions,
        loop=None,
    ):
        """
        Initialize the application service.
        """
        super().__init__(
            db_service=db_service,
            domain_adapter=domain_adapter,
            domain_publisher=domain_publisher,
            event_repository=event_repository,
            interchange_adapter=interchange_adapter,
            interchange_publisher=interchange_publisher,
            job_service=job_service,
            job_adapter=job_adapter,
            log_service=log_service,
            scheduler_adapter=scheduler_adapter,
            max_concurrent_actions=max_concurrent_actions,
            loop=loop,
        )

        # Dependencies
        self.dummy_repository = dummy_repository

        # ..categorize
        self.domain_services.extend([

        ])

        self.primary_adapters.extend([

        ])

        self.secondary_adapters.extend([
            dummy_repository,
        ])

    # Actions

    @action
    async def do_something(self, command, corr_ids=None):
        """
        Do something.
        """
        corr_ids = corr_ids if corr_ids is not None else []

        raise NotImplementedError()
