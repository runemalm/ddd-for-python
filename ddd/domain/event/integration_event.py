from ddd.domain.event.event import Event


class IntegrationEvent(Event):
    """
    An integration event.

    .. note::
        This class should never be instantiated by the user.

        Subclass and implement
        :meth:`~ddd.domain.event.event.Event.get_serialized_payload`.
    """
    def __init__(self, name, version="1", date=None, sender=None, corr_ids=None):
        super(IntegrationEvent, self).__init__(
            name=name,
            version=version,
            date=date,
            sender=sender,
            corr_ids=corr_ids,
        )
