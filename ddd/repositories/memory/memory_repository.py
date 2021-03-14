from ddd.repositories.repository import Repository


class MemoryRepository(Repository):

    def __init__(
        self,
        log_service,
        aggregate_name,
        aggregate_cls,
        translator_cls,
    ):
        super().__init__(
            log_service=log_service,
            aggregate_cls=aggregate_cls,
            translator_cls=translator_cls,
        )

        self.highest_id = 0
        self.highest_id_collector = 0
        self.records = {}

        self.aggregate_name = aggregate_name

    async def next_identity(self):
        self.highest_id += 1
        return str(self.highest_id)

    async def next_collector_identity(self):
        self.highest_id_collector += 1
        return str(self.highest_id_collector)

    # Operations

    async def _get_record(self, aggregate_id):
        if str(aggregate_id) in self.records:
            return self.records[str(aggregate_id)]
        return None

    async def _get_all_records(self):
        return self.records.values()

    async def _get_all_records_not_on_latest_version(self):
        records = []

        for r in self.records.values():
            if int(r['data']['version']) < int(self.aggregate_cls.VERSION):
                records.append(r)

        return records

    async def _save_record(self, aggregate_id, data):
        aggregate_id = str(aggregate_id)

        if aggregate_id in self.records:
            self.records.pop(aggregate_id)

        self.records[aggregate_id] = {
            'id': aggregate_id,
            'data': data,
        }

    async def _delete(self, aggregate_id):
        self.records = {
            agg_id: data for agg_id, data in self.records.items()
            if agg_id != aggregate_id
        }

    async def get_count(self):
        return len(self.records)

    async def get_single_or_raise(self):
        """
        Convenience method for tests to get a single aggregate.
        Throws exception if not exactly 1 aggregate in repository.
        """
        aggregates = await self.get_all()

        if len(aggregates) != 1:
            raise Exception(
                "Couldn't get single aggregate because there are not "
                "exactly 1 aggregate in the repository."
            )

        return aggregates[0]

    async def get_all(self):
        records = await self._get_all_records()

        records = self._migrate(records, self.aggregate_cls)

        aggregates = [
            self.aggregate_from_record(record)
            for record in records
        ]

        return aggregates

    async def delete_all(self):
        self.highest_id = 0
        self.records = {}

    # Control

    async def start(self):
        pass

    async def stop(self):
        pass

    async def connect(self):
        pass

    async def assert_table(self):
        pass

    async def disconnect(self):
        pass

    # Clean

    async def empty(self):
        self.highest_id = 0
        self.records = {}
