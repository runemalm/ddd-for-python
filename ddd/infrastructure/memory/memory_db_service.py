from ddd.infrastructure.db_service import DbService
from ddd.infrastructure.memory.memory_pool import MemoryPool


class MemoryDbService(DbService):
    """
    A memory db service.
    """
    def __init__(
        self,
        log_service,
    ):
        super().__init__(log_service=log_service)

    async def _create_conn_pool(self):
        self.log_service.info("Creating memory db pool")
        self.conn_pool = MemoryPool(max=80)
