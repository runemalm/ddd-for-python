:mod:`ddd.application.action`
==========================================

The :class:`~ddd.application.application_service.ApplicationService` contains one or more functions that implements the actions.

.. automodule:: ddd.application.action

API
---

.. autofunction:: action


Examples
--------

Decorate a function in the application service::

    @action
    async def send_tracking_email(self, command, corr_ids=None):
        """
        Send tracking email to recipient.
        """
        ...
