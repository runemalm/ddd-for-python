import asyncio
import json

import asyncpg

from ddd.infrastructure.db_service import DbService


class PostgresDbService(DbService):
    """
    A postgres db service.
    """
    def __init__(
        self,
        dsn,
        log_service,
        min_size=20,
        max_size=20,
    ):
        super().__init__(log_service=log_service)
        self.dsn = dsn
        self.min_size = min_size
        self.max_size = max_size

    async def _create_conn_pool(self):
        self.log_service.info(
            f"..creating connection pool "
            f"(min: {self.min_size}, max: {self.max_size}).."
        )

        created = False
        error = None
        backoff = 6
        retries = 0
        max_retries = 5

        async def init_conn(conn):
            await conn.set_type_codec(
                'json',
                encoder=json.dumps,
                decoder=json.loads,
                schema='pg_catalog'
            )

        while (not created) and retries < max_retries:
            try:
                pool = \
                    await asyncpg.create_pool(
                        dsn=self.dsn,
                        min_size=self.min_size,
                        max_size=self.max_size,
                        init=init_conn
                    )
                created = True
            except Exception as e:
                self.log_service.error(
                    (
                        "Failed to create connection pool of postgres db "
                        "at: {} (retrying in {} secs..), exception: {}"
                    ).
                    format(
                        self.dsn,
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
                    "App failed to create connection pool of db at: {} "
                    "after {} retries, error: {}."
                ).
                format(
                    self.dsn,
                    retries,
                    error
                )
            )

        self.conn_pool = pool
