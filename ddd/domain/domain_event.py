from ddd.domain.event import Event


class DomainEvent(Event):
    """
    An domain event.
    """
    def __init__(self, name, version="1", date=None, sender=None, corr_ids=None):
        super(DomainEvent, self).__init__(
            name=name,
            version=version,
            date=date,
            sender=sender,
            corr_ids=corr_ids,
        )
