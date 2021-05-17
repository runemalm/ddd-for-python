import asyncio
import uvloop

from abc import ABCMeta, abstractmethod

from addict import Dict
from sanic.request import RequestParameters

from ddd.utils.dep_mgr import DependencyManager
from ddd.tests.base_test_case import BaseTestCase


class ActionTestCase(BaseTestCase, metaclass=ABCMeta):

    def __init__(self, env_file_path=None, methodName='runTest'):
        super().__init__(
            env_file_path=env_file_path,
            methodName=methodName,
        )

        # Configure
        self.maxDiff = None

    async def asyncSetUp(self):
        await super().asyncSetUp()

        # Vars
        self.service = None

        # Loop
        self.loop = uvloop.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Deps manager
        self._create_deps_manager()

        # Register service
        self.deps.set_service(self.get_service())

        # Start service
        await self.get_service().start()

    async def asyncTearDown(self):
        await super().asyncTearDown()

        # TODO: Delete all events in events repository, when not memory rep?

        await self.get_service().stop()

    # Dependencies

    def _create_deps_manager(self):
        self.deps = DependencyManager(
            config=self.config,
            loop=self.loop,
        )

    @abstractmethod
    def get_service(self):
        pass

    # Events

    async def simulate_domain_event(self, event):
        await self.deps.get_domain_publisher().flush(event=event)

        # In case we run test with kafka or azure, we need delay
        # to allow for delivery.
        if self.config.pubsub.domain.provider == "kafka":
            await asyncio.sleep(0.01)
        elif self.config.pubsub.domain.provider == "azure":
            await asyncio.sleep(1.5)

    async def simulate_integration_event(self, event):
        await self.deps.get_interchange_publisher().flush(event=event)

        # In case we run test with kafka or azure, we need delay
        # to allow for delivery.
        if self.config.pubsub.interchange.provider == "kafka":
            await asyncio.sleep(0.01)
        elif self.config.pubsub.interchange.provider == "azure":
            await asyncio.sleep(1.5)

    # Requests

    def _create_request(
        self,
        token=None,
        headers=None,
        query_args=None,
        form=None,
        body=None,
        json_=None,
    ):
        """
        Create a sanice request for use by tests.
        """
        headers = headers if headers is not None else {}
        query_args = query_args if query_args is not None else {}
        form = form if form is not None else {}

        if json_ is not None and body is not None:
            raise Exception("Pass either 'json_' or 'body'.")

        if json_ is not None:
            body = json.dumps(json_)
        else:
            body = body if body is not None else ""

        headers.update({
            'X-TOKEN': token,
        })

        request = \
            Dict({
                'headers': headers,
                'args': query_args,
                'form': form,
                'body': body.encode('utf-8'),
                'json': json_,
            })

        request.args = \
            RequestParameters(
                {
                    k: (v if isinstance(v, list) else [v])
                    for k, v in query_args.items()
                }
            )

        return request

    # Assert

    def assertDomainEventPublished(self, event, ignore_fields=None):
        """
        Asserts that the 'event' domain event was published.
        """
        ignore_fields = ignore_fields if ignore_fields is not None else []

        if 'date' not in ignore_fields:
            ignore_fields.append('date')

        self.assertTrue(
            self.deps.get_domain_publisher().has_flushed(
                event=event,
                ignore_fields=ignore_fields
            ),
            f"Expected domain event to "
            f"have been published: '{event.name}'"
        )

    def assertDomainEventNotPublished(self, event, ignore_fields=None):
        """
        Asserts that the 'event' domain event was NOT published.
        """
        ignore_fields = ignore_fields if ignore_fields is not None else []

        if 'date' not in ignore_fields:
            ignore_fields.append('date')

        self.assertFalse(
            self.deps.get_domain_publisher().has_flushed(
                event=event,
                ignore_fields=ignore_fields
            ),
            f"Expected domain event to NOT "
            f"have been published: '{event.name}'"
        )

    def assertIntegrationEventPublished(self, event, ignore_fields=None):
        """
        Asserts that the 'event' integration event was published.
        """
        ignore_fields = ignore_fields if ignore_fields is not None else []

        if 'date' not in ignore_fields:
            ignore_fields.append('date')

        self.assertTrue(
            self.deps.get_interchange_publisher().has_flushed(
            event=event,
                ignore_fields=ignore_fields
            ),
            f"Expected integration event to "
            f"have been published: '{event.name}'"
        )
