:mod:`ddd.infrastructure.db_service.postgres_db_service`
========================================================

.. automodule:: ddd.infrastructure.db_service.postgres_db_service

API
---

.. autoclass:: PostgresDbService
    :members: start, stop
    :show-inheritance:


Examples
--------

Create a ``postgres_db_service`` and ``start`` it::

    from ddd.infrastructure.db_service.postgres_db_service import PostgresDbService


    log_service = ...

    db_service = \
        PostgresDbService(
            dsn="postgresql://localhost:5432",
            log_service=log_service,
            min_size=20,
            max_size=20,
        )

    await db_service.start()
