:mod:`ddd.infrastructure.db_service.memory_postgres_db_service`
===============================================================

.. automodule:: ddd.infrastructure.db_service.memory_postgres_db_service

API
---

.. autoclass:: MemoryPostgresDbService
    :members:
    :show-inheritance:


Examples
--------

Create a ``memory_postgres_db_service`` and ``start`` it::

    from ddd.infrastructure.db_service.memory_postgres_db_service import MemoryPostgresDbService


    log_service = ...

    db_service = \
        MemoryPostgresDbService(
            log_service=log_service,
            min_size=20,
            max_size=20,
        )

    await db_service.start()
