import asyncio
import uvloop

from ddd.infrastructure.container import Container
from ddd.utils.utils import load_env_file

from webshop.utils.utils import read_config

from webshop.utils.dep_mgr import DependencyManager

from webshop.application.webshop_application_service import WebshopApplicationService


if __name__ == "__main__":
    """
    This is the container entry point.    
    Creates the app and runs it in the container.
    """
    # Config
    load_env_file()
    config = read_config()

    # Loop
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)

    # Dependencies
    deps = \
        DependencyManager(
            config=config,
            loop=loop,
        )

    # Create app
    app_service = \
        WebshopApplicationService(
            db_service=deps.get_db_service(),
            domain_adapter=deps.get_domain_adapter(),
            domain_publisher=deps.get_domain_publisher(),
            event_repository=deps.get_event_repository(),
            interchange_adapter=deps.get_interchange_adapter(),
            interchange_publisher=deps.get_interchange_publisher(),
            job_adapter=deps.get_job_adapter(),
            job_service=deps.get_job_service(),
            log_service=deps.get_log_service(),
            scheduler_adapter=deps.get_scheduler_adapter(),
            max_concurrent_actions=config.max_concurrent_actions,
        )

    deps.set_service(app_service)

    # Create container
    container = \
        Container(
            app_service=app_service,
            log_service=deps.get_log_service(),
        )

    # ..run
    loop.run_until_complete(container.run())
    loop.close()
