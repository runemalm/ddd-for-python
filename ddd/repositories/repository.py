import arrow
import dateutil

from abc import abstractmethod


class Repository(object):

    def __init__(
        self,
        log_service,
        aggregate_cls,
        translator_cls,
    ):
        super().__init__()
        self.log_service = log_service
        self.aggregate_cls = aggregate_cls
        self.translator_cls = translator_cls

    # Init

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def assert_table(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    # Control

    async def start(self):
        await self.connect()
        await self.assert_table()

    async def stop(self):
        await self.disconnect()

    # Operations

    async def _get(self, aggregate_id):
        record = await self._get_record(aggregate_id=aggregate_id)

        aggregate = None

        if record:
            aggregate = self.aggregate_from_record(record)

        return aggregate

    async def get_all(self):
        records = await self._get_all_records()
        aggregates = [self.aggregate_from_record(record) for record in records]
        return aggregates

    async def get_all_not_on_latest_version(self):
        records = await self._get_all_records_not_on_latest_version()
        records = self._migrate(records, self.aggregate_cls)
        aggregates = [self.aggregate_from_record(record) for record in records]
        return aggregates

    @abstractmethod
    async def _get_record(self, aggregate_id):
        pass

    @abstractmethod
    async def _get_all_records(self):
        pass

    @abstractmethod
    async def _get_all_records_not_on_latest_version(self):
        pass

    @abstractmethod
    async def next_identity(self):
        pass

    async def _save(self, aggregate_id, aggregate):
        await self._save_record(aggregate_id, self._serialize(aggregate))

    @abstractmethod
    async def _save_record(self, aggregate_id, data):
        pass

    # Dates

    def datetime_from_iso8601(self, iso8601, tz_if_missing="Europe/Stockholm"):
        if iso8601 is None:
            return None
        
        # Contains timezone?
        date = dateutil.parser.parse(iso8601)
        
        if date.tzinfo is None:
            # ..no, use default
            date = arrow.get(
                iso8601,
                "YYYY-MM-DDTHH:mm:ss.SSSSSSZZ",
                tzinfo=tz_if_missing
            )
            
        else:
            # ..yes, use it
            date = arrow.get(
                iso8601,
                "YYYY-MM-DDTHH:mm:ss.SSSSSSZZ"
            )
        
        return date

    def now(self, tz="Europe/Stockholm"):
        now = arrow.utcnow().to(tz)
        return now

    def now_iso8601(self, tz="Europe/Stockholm"):
        string = self.now(tz).format("YYYY-MM-DDTHH:mm:ss.SSSSSSZZ")
        return string

    # Serialization / Deserialization

    def aggregate_from_record(self, record):
        aggregate = self.translator_cls.from_record(record)
        return aggregate

    def _serialize(self, aggregate):
        """
        Serializes an aggregate by turning it into a dict.
        """
        data = self.translator_cls(aggregate).to_domain()
        return data

    # Migration

    def _migrate(self, records, cls):
        """
        Migrate the record to latest version.
        """
        migrated = []

        if len(records):
            if not hasattr(cls, "VERSION"):
                raise Exception(
                    f"Couldn't migrate entity. "
                    f"The '{cls}' class is missing 'VERSION'."
                )

        for r in records:

            versions = \
                self._get_versions_to_migrate_to(
                    record=r,
                    cls=cls
                )

            if versions.stop > 0:
                prev = versions.start - 1

                for next_ in range(versions.start, versions.stop + 1):
                    func_name = f"_migrate_v{prev}_to_v{next_}"
                    func = getattr(self, func_name)

                    if not func:
                        raise Exception(
                            f"Couldn't migrate entity. "
                            f"The '{cls}' class is missing the "
                            f"'{func_name}' function"
                        )

                    # Log
                    self.log_service.debug(
                        f"Migrating '{self.aggregate_cls.__name__}' "
                        f"from 'v{prev}' to 'v{next_}'."
                    )

                    # Migrate record to next version
                    r = func(record=r)

                    # Inc. version
                    r['data']['version'] = str(next_)

                    prev = next_

            migrated.append(r)

        return migrated

    def _get_versions_to_migrate_to(self, record, cls):
        """
        Get a range of consecutive versions to migrate to.
        """
        latest = int(cls.VERSION)
        current = self._get_version_from_record(record)

        if latest == current:
            versions = range(0, 0)
        else:
            versions = range(current + 1, latest)

        return versions

    def _get_version_from_record(self, record):
        version = int(record['data']['version'])
        return version
