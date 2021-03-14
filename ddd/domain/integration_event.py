from ddd.domain.event import Event


class IntegrationEvent(Event):
    """
    An integration event.
    """
    def __init__(self, name, version="1", date=None, sender=None, corr_ids=None):
        super(IntegrationEvent, self).__init__(
            name=name,
            version=version,
            date=date,
            sender=sender,
            corr_ids=corr_ids,
        )
