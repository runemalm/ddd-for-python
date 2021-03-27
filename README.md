## DDD for Python  

This is a framework for developing apps based on domain-driven design principles.
 The design is inspired by Vaughn Vernon's reference implementation of Eric Evans DDD concept in Java.

### Purpose:

The goal of this project is to provide a complete framework for implementing DDD bounded contexts in Python.
Star/follow the project to receive notification when version 1.0.0 is released.

Full documentation will be available in version 1.0.0. There's a code example for a 'shipping' context in the 'examples' folder you can look at meanwhile, if you want to try it out already today.

I would love to get your feedback!

### Theory: 
  
If you are new to DDD, the following sources are recommended:
  
- [Domain-Driven Design: Tackling Complexity in the Heart of Software - Eric Evans](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)  
- [Implementing Domain-Driven Design - Vaughn Vernon](https://www.amazon.com/Implementing-Domain-Driven-Design-Vaughn-Vernon/dp/0321834577)  

### Supported Python Versions:

- Tested with python 3.8.5.
- Should work with any version >= 3.8.0 (not tested).
  
### Installation:
  
```bash
$ pip install ddd-for-python
```
  
### Example:

```python
# This is the "main.py" file that
# starts the bounded context in a container.

from ddd.infrastructure.config import Config
from ddd.infrastructure.container import Container

from shipping.utils.dep_mgr import DependencyManager
from shipping.application.shipping_application_service import \
    ShippingApplicationService


if __name__ == "__main__":
    """
    This is the container entry point.    
    Creates the application service and runs it in the container.
    """
    
    # Config
    config = Config()

    # Dependency manager
    dep_mgr = \
        DependencyManager(
            config=config,
        )

    # Application service
    service = \
        ShippingApplicationService(
            customer_repository=dep_mgr.get_customer_repository(),
            db_service=dep_mgr.get_db_service(),
            domain_adapter=dep_mgr.get_domain_adapter(),
            domain_publisher=dep_mgr.get_domain_publisher(),
            event_repository=dep_mgr.get_event_repository(),
            interchange_adapter=dep_mgr.get_interchange_adapter(),
            interchange_publisher=dep_mgr.get_interchange_publisher(),
            job_adapter=dep_mgr.get_job_adapter(),
            job_service=dep_mgr.get_job_service(),
            log_service=dep_mgr.get_log_service(),
            scheduler_adapter=dep_mgr.get_scheduler_adapter(),
            shipment_repository=dep_mgr.get_shipment_repository(),
            max_concurrent_actions=config.max_concurrent_actions,
            loop=config.loop.instance,
        )

    # ..register
    dep_mgr.set_service(service)

    # Container
    container = \
        Container(
            service=service,
            log_service=dep_mgr.get_log_service(),
        )

    # ..run
    loop = config.loop.instance
    loop.run_until_complete(container.run())
    loop.close()
```

For the full code, see: "examples/webshop/shipping".
  
### Documentation:
  
The documentation is coming shortly.
  
### Release Notes:

**0.9.3** - 2021-03-27
- Search env file from cwd by default in tests, (when no path specified).
- Refactor Task class to make it more simple.
- Refactor the configuration solution by adding a Config class.
- Add example code for 'shipping' context of a webshop application.
- Add get_all_jobs() and get_job_count() to scheduler adapter & service.
- Add missing call to _migrate() in a couple of Repository class functions.

**0.9.2** - 2021-03-15
- Fix a bug where env file wasn't loaded in certain circumstances.

**0.9.1** - 2021-03-14
- First release.
