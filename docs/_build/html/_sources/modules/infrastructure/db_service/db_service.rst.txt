:mod:`ddd.infrastructure.db_service`
====================================

The db service is used to acquire connections to the database.

You will not use this base class directly. Instead, you use one of the implementations:
:class:`~ddd.infrastructure.db_service.postgres_db_service.PostgresDbService`
:class:`~ddd.infrastructure.db_service.memory_db_service.MemoryDbService` or
:class:`~ddd.infrastructure.db_service.memory_postgres_db_service.MemoryPostgresDbService`.

Look at the documentation to figure out which one to use.


.. automodule:: ddd.infrastructure.db_service.db_service

API
---

.. autoclass:: DbService
    :members:
