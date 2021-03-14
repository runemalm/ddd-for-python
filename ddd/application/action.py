import asyncio
import copy
import uuid

from ddd.application.domain_registry import DomainRegistry
from ddd.domain.exceptions import DomainException


def action(func):
    """
    A decorator for the application service's "action" methods.

    Calls the wrapped method inside a transaction. Then saves any
    published events to the database.

    If transaction is committed (not rolled back), the events are
    actually published and then deleted from the database.

    The flow described above makes sure state is persisted and events
    are published atomically (either both happens or nothing). This
    assures us the overall system state is consistent.
    """
    async def func_wrapper(self, *args, **kwargs):
        async with self.action_sem:
            task_id = id(asyncio.current_task())
            action_id = uuid.uuid4().hex
            domain_exception = None
            result = None

            # Get dependencies
            domain_publisher = self.domain_publisher
            interchange_publisher = self.interchange_publisher
            event_repository = self.event_repository

            # Log
            command = None

            if 'command' in kwargs:
                command = copy.deepcopy(kwargs.get('command')).__dict__
                if 'token' in command:
                    command['token'] = "(hidden)"
                if 'password' in command:
                    command['password'] = "(hidden)"
                if 'new_password' in command:
                    command['new_password'] = "(hidden)"

            if 'corr_ids' in kwargs and kwargs['corr_ids']:
                corr_ids = command['corr_ids']
            else:
                corr_ids = []

            self.log_service.info(
                f"[ ACTION ]: {func.__name__}",
                extra={
                    'extra': {
                        'command': command,
                    },
                    'corr_ids': corr_ids,
                }
            )

            try:
                async with self.db_service.conn_pool.acquire() as conn:
                    DomainRegistry.get_instance().task_db_conns[task_id] = conn

                    # BEGIN TRANSACTION
                    async with conn.transaction():

                        # Run action
                        try:
                            result = await func(self, *args, **kwargs)
                        except Exception as e:
                            if not isinstance(e, DomainException):
                                raise Exception(
                                    f"Failed to run action, "
                                    f"exception: {str(e)}"
                                )
                            domain_exception = e

                        # Save domain events
                        try:
                            published = domain_publisher.get_published()
                            if len(published):
                                await event_repository.save_all(
                                    action_id=action_id,
                                    events=published,
                                    event_type="domain"
                                )
                            domain_publisher.clear_published()
                        except Exception as e:
                            raise Exception(
                                f"Failed to persist domain events, "
                                f"exception: {str(e)}"
                            )

                        # Save integration events
                        try:
                            published = interchange_publisher.get_published()
                            if len(published):
                                await event_repository.save_all(
                                    action_id=action_id,
                                    events=published,
                                    event_type="integration"
                                )
                            interchange_publisher.clear_published()
                        except Exception as e:
                            raise Exception(
                                f"Failed to persist interchange events, "
                                f"exception: {str(e)}"
                            )
                    # END TRANSACTION

                    # Flush domain events
                    try:
                        events = await event_repository.get_unpublished(
                            action_id=action_id,
                            event_type="domain"
                        )
                        for event in events:
                            self.log_service.debug(
                                f"Flushing domain event: '{event.name}'"
                            )
                            await domain_publisher.flush(event)

                        await event_repository.delete_all(
                            action_id=action_id,
                            event_type="domain"
                        )

                    except Exception as e:
                        raise Exception(
                            f"Failed to publish domain events, "
                            f"exception: {str(e)}"
                        )

                    # Flush integration events
                    try:
                        events = \
                            await event_repository.get_unpublished(
                                action_id=action_id,
                                event_type="integration"
                            )
                        for event in events:
                            self.log_service.debug(
                                f"Flushing interchange event: '{event.name}'"
                            )
                            await interchange_publisher.flush(event)

                        await \
                            event_repository.delete_all(
                                action_id=action_id,
                                event_type="integration"
                            )

                    except Exception as e:
                        raise Exception(
                            f"Failed to publish integration events "
                            f"with exception: {str(e)}"
                        )

            finally:

                # Remove db conn reference
                if task_id in DomainRegistry.get_instance().task_db_conns:
                    del DomainRegistry.get_instance().task_db_conns[task_id]

            # Raise action exception, if occured
            if domain_exception:
                raise domain_exception

            return result

    return func_wrapper
