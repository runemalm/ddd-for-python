import asyncio
import uuid

from abc import ABCMeta

from ddd.repositories.repository import Repository


class PostgresRepository(Repository, metaclass=ABCMeta):

    def __init__(
        self,
        db_service,
        log_service,
        aggregate_cls,
        translator_cls,
        table_name,
        dsn,
        loop=None,
    ):
        super().__init__(
            log_service=log_service,
            aggregate_cls=aggregate_cls,
            translator_cls=translator_cls,
        )

        self.db_service = db_service
        self.table_name = table_name
        self.dsn = dsn
        self.loop = loop if loop is not None else asyncio.get_event_loop()

    # Operations

    async def _delete(self, aggregate_id):
        async with self.db_service.conn_pool.acquire() as conn:
            await conn.execute(
                """
                DELETE FROM {} WHERE id = $1
                """.
                format(
                    self.table_name
                ),
                str(aggregate_id)
            )

    async def _get_record(self, aggregate_id):
        async with self.db_service.conn_pool.acquire() as conn:
            record = await conn.fetchrow(
                """
                SELECT * FROM {} WHERE id = $1
                """.
                format(
                    self.table_name
                ),
                str(aggregate_id)
            )

            return record

    async def _get_all_records(self):
        async with self.db_service.conn_pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT * FROM {}
                """.
                format(
                    self.table_name
                )
            )
            return records

    async def _get_all_records_not_on_latest_version(self):
        async with self.db_service.conn_pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT * FROM {} WHERE (data->>'version')::int < $1
                """.
                format(
                    self.table_name
                ),
                int(self.aggregate_cls.VERSION)
            )
            return records

    async def delete_all(self):
        await self.assert_table()

        async with self.db_service.conn_pool.acquire() as conn:
            await conn.execute(
                """
                DELETE FROM {}
                """.
                format(
                    self.table_name
                )
            )
            return True

    async def get_single_or_raise(self):
        """
        Convenience method for tests to get a single aggregate.
        Throws exception if not exactly 1 aggregate in repository.
        """
        async with self.db_service.conn_pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT * FROM {}
                """.
                format(
                    self.table_name
                )
            )
            aggregates = [
                self.aggregate_from_record(record) for record in records
            ]

            if len(aggregates) != 1:
                raise Exception(
                    "Couldn't get single aggregate because there are not "
                    "exactly 1 aggregate in the repository."
                )

            return aggregates[0]

    async def get_count(self):
        """
        Get the total number of aggregates.
        """
        async with self.db_service.conn_pool.acquire() as conn:
            count = await conn.fetchval(
                """
                SELECT COUNT(*) FROM {}
                """.
                format(
                    self.table_name
                )
            )
            return count

    async def next_identity(self):
        return uuid.uuid4().hex

    async def _save_record(self, aggregate_id, data):
        async with self.db_service.conn_pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO {} (id, data)
                VALUES
                (
                    $1,
                    $2
                ) 
                ON CONFLICT (id)
                DO
                UPDATE
                    SET data = $2
                """.
                format(
                    self.table_name
                ),
                str(aggregate_id),
                data,
            )

    def _filter_by_property(self, records, property, values):
        return \
            self._filter_by_properties(
                records=records,
                properties={
                    property: values,
                },
            )

    def _filter_by_properties(self, records, properties):
        filtered = []

        for record in records:
            for name, values in properties.items():
                if name not in record['data']:
                    raise Exception(
                        f"Couldn't filter records by property values in "
                        f"postgres adapter. The record has no property "
                        f"named '{name}'."
                    )
                if record['data'][name] in values:
                    filtered.append(record)

        return filtered

    # Connection

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    # Table

    async def assert_table(self):
        async with self.db_service.conn_pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS {}(
                    id VARCHAR UNIQUE NOT NULL,
                    data json NOT NULL
                )
                """.
                format(
                    self.table_name
                )
            )
