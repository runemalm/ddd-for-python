import asyncio

from asyncio import Semaphore


class ApplicationService(object):
    """
    An application service.
    Extend this to add your own dependencies.
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
        max_concurrent_actions=40,
        loop=None,
    ):
        super().__init__()

        # Dependencies
        self.db_service = db_service
        self.domain_adapter = domain_adapter
        self.domain_publisher = domain_publisher
        self.event_repository = event_repository
        self.interchange_adapter = interchange_adapter
        self.interchange_publisher = interchange_publisher
        self.job_service = job_service
        self.job_adapter = job_adapter
        self.log_service = log_service
        self.scheduler_adapter = scheduler_adapter

        # ..categorize
        self.primary_adapters = [
            domain_adapter,
            interchange_adapter,
            job_adapter,
        ]

        self.secondary_adapters = []

        self.domain_services = []

        self.infrastructure_services = [
            db_service,
            job_service,
            log_service,
        ]

        # Vars
        self.loop = loop if loop else asyncio.get_event_loop()
        self.max_concurrent_actions = max_concurrent_actions

        # Actions
        self._create_action_sem()

    # Container

    def _create_action_sem(self):
        """
        Create the semaphore used to throttle concurrent actions.
        This number affects e.g. database connections opened.
        """
        self.action_sem = Semaphore(self.max_concurrent_actions)

    # Control

    async def start(self):
        """
        Starts the service.
        """
        self.log_service.info("Starting application service.")

        await self._start_domain_publisher()
        await self._start_interchange_publisher()
        await self._start_domain_services()
        await self._start_infrastructure_services()
        await self._start_secondary_adapters()
        await self._start_primary_adapters()

        self.log_service.info("Application service started.")

    async def stop(self):
        """
        Stops the service.
        """
        self.log_service.info("Stopping application service.")

        await self._stop_domain_publisher()
        await self._stop_interchange_publisher()
        await self._stop_primary_adapters()
        await self._stop_secondary_adapters()
        await self._stop_domain_services()
        await self._stop_infrastructure_services()

        self.log_service.info("Stopping application service.")

    async def _start_domain_publisher(self):
        """
        Starts the domain publisher.
        """
        self.log_service.info("Starting domain publisher.")

        await self.domain_publisher.start()

    async def _start_interchange_publisher(self):
        """
        Starts the interchange publisher.
        """
        self.log_service.info("Starting interchange publisher.")

        await self.interchange_publisher.start()

    async def _start_primary_adapters(self):
        """
        Starts the primary adapters.
        """
        self.log_service.info("Starting primary adapters..")

        for adapter in self.primary_adapters:
            if hasattr(adapter, "start"):
                self.log_service.info(
                    f"..starting {adapter.__class__.__name__}"
                )
                await adapter.start()

    async def _start_secondary_adapters(self):
        """
        Starts the secondary adapters.
        """
        self.log_service.info("Starting secondary adapters..")

        for adapter in self.secondary_adapters:
            if hasattr(adapter, "start"):
                self.log_service.info(
                    f"..starting {adapter.__class__.__name__}"
                )
                await adapter.start()

    async def _stop_interchange_publisher(self):
        """
        Stop the interchange publisher.
        """
        self.log_service.info("Stopping interchange publisher.")

        await self.interchange_publisher.stop()

    async def _stop_domain_publisher(self):
        """
        Stop the domain publisher.
        """
        self.log_service.info("Stopping domain publisher.")

        await self.domain_publisher.stop()

    async def _stop_primary_adapters(self):
        """
        Stops the primary adapters.
        """
        self.log_service.info("Stopping primary adapters..")

        for adapter in self.primary_adapters:
            if hasattr(adapter, "stop"):
                self.log_service.info(
                    f"..stopping {adapter.__class__.__name__}."
                )
                await adapter.stop()

    async def _stop_secondary_adapters(self):
        """
        Stops the secondary adapters.
        """
        self.log_service.info("Stopping secondary adapters..")

        for adapter in self.secondary_adapters:
            if hasattr(adapter, "stop"):
                self.log_service.info(
                    f"..stopping {adapter.__class__.__name__}."
                )
                await adapter.stop()

    async def _start_domain_services(self):
        """
        Starts the domain services.
        """
        self.log_service.info("Starting domain services..")

        for service in self.domain_services:
            if hasattr(service, "start"):
                self.log_service.info(
                    f"..starting {service.__class__.__name__}"
                )
                await service.start()

    async def _start_infrastructure_services(self):
        """
        Starts the infrastructure services.
        """
        self.log_service.info("Starting infrastructure services..")

        for service in self.infrastructure_services:
            if hasattr(service, "start"):
                self.log_service.info(
                    f"..starting {service.__class__.__name__}"
                )
                await service.start()

    async def _stop_domain_services(self):
        """
        Stops the domain services.
        """
        self.log_service.info("Stopping domain services..")

        for service in self.domain_services:
            if hasattr(service, "stop"):
                self.log_service.info(
                    f"..stopping {service.__class__.__name__}"
                )
                await service.stop()

    async def _stop_infrastructure_services(self):
        """
        Stops the infrastructure services.
        """
        self.log_service.info("Stopping infrastructure services..")

        for service in self.infrastructure_services:
            if hasattr(service, "stop"):
                self.log_service.info(
                    f"..stopping {service.__class__.__name__}"
                )
                await service.stop()
