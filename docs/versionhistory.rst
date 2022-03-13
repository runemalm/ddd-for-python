###############
Version history
###############

**0.9.5**

- Added documentation.
- Moved db_service related classes.
- Moved event related classes.
- Added :class:`~ddd.infrastructure.db_service.memory_postgres_db_service.MemoryPostgresDbService` to be able to run tests against an in-memory postgres database.
- Fixed bug: container kwarg in example main.py (thanks euri10).

.. _documentation: https://ddd-for-python.readthedocs.io/en/latest/

**0.9.4**

- Added ``context`` to log service's log messages.
- Moveed record filtering methods to base repository class.
- Added ``uses_service`` to Task class. Deprecate ``makes_requests``.

**0.9.3**

- Searching env file from cwd by default in tests, (when no path specified).
- Refactored Task class to make it more simple.
- Refactored the configuration solution by adding a Config class.
- Added example code for ``shipping`` context of a webshop application.
- Added get_all_jobs() and get_job_count() to scheduler adapter & service.
- Added missing call to _migrate() in a couple of Repository class functions.

**0.9.2**

- Fixed bug: Env file wasn't loaded in certain circumstances.

**0.9.1**

- Initial commit.
