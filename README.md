## DDD for Python  

This is a framework for developing apps based on domain-driven design principles.
 
The design is inspired by Vaughn Vernon's reference implementation in Java.

Also, of course, the DDD principles as defined by Eric Evans.

You can probably find a little bit design borrowed from django in there as well.

### Purpose:

The goal of this project is to provide a complete framework for implementing DDD bounded contexts in Python.

Star/follow the project to receive notification when version 1.0.0 is released, which will be soon.

Feel free to try the framework out already now though, I'd love to get your feedback.

Documentation is also on the way in version 1.0.0, as well as full test coverage.

### Theory: 
  
If you are new to DDD, the following sources are recommended:
  
- [Domain-Driven Design: Tackling Complexity in the Heart of Software - Eric Evans](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)  
- [Implementing Domain-Driven Design - Vaughn Vernon](https://www.amazon.com/Implementing-Domain-Driven-Design-Vaughn-Vernon/dp/0321834577)  
  
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
    Creates the app and runs it in the container.
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
  
### Change Log:  

| | | |  
|-|-|-|  
| __Date__   | __Version__ | __Changes__                                                                |
| 2021-XX-XX | 0.9.X       | Search env file from cwd by default in tests, (when no path specified).    |
|            |             | Make _login() method of Task class abstract.                               |
|            |             | Refactor config concept (create 'Config' class).                           |
| 2021-03-15 | 0.9.2       | Fix bug where env file wasn't loaded.                                      |
| 2021-03-14 | 0.9.1       | Initial release.                                                           |
