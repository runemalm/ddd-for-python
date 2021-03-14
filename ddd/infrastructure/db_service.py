from abc import ABCMeta, abstractmethod

from ddd.infrastructure.infrastructure_service import InfrastructureService


class DbService(InfrastructureService, metaclass=ABCMeta):
    """
    A db service base class.
    """
    def __init__(
        self,
        log_service,
    ):
        super().__init__(log_service=log_service)
        self.conn_pool = None

    @abstractmethod
    async def _create_conn_pool(self):
        pass

    async def start(self):
        self.log_service.info("..starting db service")
        await self._create_conn_pool()

    async def stop(self):
        self.log_service.info("..stopping db service")
        await self.conn_pool.close()
