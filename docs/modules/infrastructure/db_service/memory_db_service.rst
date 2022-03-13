:mod:`ddd.infrastructure.db_service.memory_db_service`
======================================================

.. automodule:: ddd.infrastructure.db_service.memory_db_service

API
---

.. autoclass:: MemoryDbService
    :members:
    :show-inheritance:


Examples
--------

Create a ``memory_db_service`` and ``start`` it::

    from ddd.infrastructure.db_service.memory_db_service import MemoryDbService


    log_service = ...

    db_service = \
        MemoryDbService(
            log_service=log_service,
        )

    await db_service.start()
