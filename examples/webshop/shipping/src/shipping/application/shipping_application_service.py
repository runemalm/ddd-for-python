from ddd.application.application_service import ApplicationService
from ddd.application.action import action


class ShippingApplicationService(ApplicationService):
    """
    This is the context's application service.
    """
    def __init__(
        self,
        customer_repository,
        db_service,
        domain_adapter,
        domain_publisher,
        event_repository,
        interchange_adapter,
        interchange_publisher,
        job_adapter,
        job_service,
        log_service,
        scheduler_adapter,
        shipment_repository,
        max_concurrent_actions,
        loop,
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
            job_adapter=job_adapter,
            job_service=job_service,
            log_service=log_service,
            scheduler_adapter=scheduler_adapter,
            max_concurrent_actions=max_concurrent_actions,
            loop=loop,
        )

        # References
        self.customer_repository = customer_repository
        self.shipment_repository = shipment_repository

        # Classify deps
        self.domain_services.extend([

        ])

        self.primary_adapters.extend([

        ])

        self.secondary_adapters.extend([
            customer_repository,
            shipment_repository,
        ])

    # Actions

    @action
    async def send_tracking_email(self, command, corr_ids=None):
        """
        Send tracking email to recipient.
        """
        corr_ids = corr_ids if corr_ids is not None else []

        raise NotImplementedError()
