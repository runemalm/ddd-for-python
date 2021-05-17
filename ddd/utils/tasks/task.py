import aiosonic
import argparse

from abc import ABCMeta, abstractmethod


class Task(object, metaclass=ABCMeta):
    """
    A base class for tasks.
    """
    def __init__(
        self,
        config,
        deps_mgr,
        args_str,
        makes_requests=False,   # deprecated, (use commands on service instead)
        uses_service=False
    ):
        super().__init__()

        self.config = config
        self.deps_mgr = deps_mgr
        self.args_str = args_str
        self.makes_requests = makes_requests
        self.uses_service = uses_service

        self._create_args_parser()
        self.add_args(parser=self.parser)
        self._parse_args()

        self.client = None
        self.service = None

    # Interface

    @abstractmethod
    def add_args(self, parser):
        """
        Override this method in subclasses.
        """
        pass

    @abstractmethod
    async def run(self):
        """
        Override this method in subclasses.
        """
        pass

    # Init

    def _create_args_parser(self):
        self.parser = argparse.ArgumentParser()

    def _parse_args(self):
        args = []

        if len(self.args_str) > 0:
            args = self.args_str.split(" ")

        self.args = self.parser.parse_args(args=args)

    # Run

    async def _run(self):
        if "-h" in self.args or "--help" in self.args:
            self.parser.print_help()
        else:
            await self.initialize()
            await self.run()

    async def initialize(self):
        """
        Override this method if you need to do some initialization
        in your subclass before run() is called,
        (for example initiate state variables).
        """
        # Client
        if self.makes_requests:
            self.client = aiosonic.HTTPClient()
            await self._login()

        # Service
        if self.uses_service:
            await self._create_service()
            await self._register_service()
            await self._start_service()

    # HTTP

    @abstractmethod
    async def _login(self):
        pass

    # Application Service

    @abstractmethod
    async def _create_service(self):
        pass

    @abstractmethod
    async def _register_service(self):
        pass

    async def _start_service(self):
        await self.service.start()
