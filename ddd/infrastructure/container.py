import asyncio
import signal


class Container(object):
    """
    A container for hosting an application service.
    """
    def __init__(self, app_service, log_service, loop=None):
        super().__init__()

        # Deps
        self.app_service = app_service
        self.log_service = log_service
        self.loop = loop if loop else asyncio.get_event_loop()

        # Vars
        self.stop_sem = None

        # Docker
        self._create_stop_semaphore()
        self._subscribe_to_signals()

    # Docker

    def _create_stop_semaphore(self):
        """
        Create the stop semaphore that we will block on after application
        service has been started.

        Acquiring the semaphore means the container has been ordered to stop.
        """
        self.stop_sem = asyncio.Event()

    def _subscribe_to_signals(self):
        """
        Subscribe to SIGINT (ctrl + c) and SIGTERM (docker stop).
        """
        for signal_name in ('SIGINT', 'SIGTERM'):
            self.loop.add_signal_handler(
                getattr(signal, signal_name),
                lambda: self.loop.create_task(self._handle_signal(signal_name))
            )

    async def _handle_signal(self, signal_name):
        """
        Handler for process signals.
        """
        self.log_service.debug(f"Received system signal: '{signal_name}'.")

        if signal_name in ['SIGTERM', 'SIGKILL']:
            self.stop_sem.set()

    # Run

    async def run(self):
        """
        Run the app, (called on container start).
        """
        await self.app_service.start()
        await self.wait_for_stop()
        await self.stop()

    async def wait_for_stop(self):
        """
        Block waiting for termination/stop signals.
        """
        self.log_service.info("Waiting for stop/term signals..")
        await self.stop_sem.wait()

    async def stop(self):
        self.log_service.info("Stopping app..")
        await self.app_service.stop()
