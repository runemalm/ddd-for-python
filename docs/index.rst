ddd-for-python
============

Welcome to the ddd-for-python framework.

This framework is used to do DDD with python. Below is an example of a bounded context implemented with ddd-for-python.

Check out the :doc:`user guide<gettingstarted>` to get started building your own contexts.
  

Example
=======

.. code-block:: python

    from ddd.application.config import Config
    from ddd.infrastructure.container import Container

    from shipping.utils.dep_mgr import DependencyManager
    from shipping.application.shipping_application_service import \
    ShippingApplicationService


    if __name__ == "__main__":
        
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
                app_service=service,
                log_service=dep_mgr.get_log_service(),
            )

        # ..run
        loop = config.loop.instance
        loop.run_until_complete(container.run())
        loop.close()

.. gettingstarted-docs:
.. toctree::
  :maxdepth: 1
  :caption: User guide

  gettingstarted

.. versionhistory-docs:
.. toctree::
  :maxdepth: 1
  :caption: Releases

  versionhistory

.. troubleshooting-docs:
.. toctree::
  :maxdepth: 1
  :caption: Troubleshooting

  troubleshooting

.. community-docs:
.. toctree::
  :maxdepth: 1
  :caption: Community

  community

.. apireference-docs:
.. toctree::
  :maxdepth: 1
  :caption: API Reference

  py-modindex
