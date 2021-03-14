import arrow
import copy

from abc import ABCMeta, abstractmethod

from ddd.utils.utils import get_for_compare


class Event(object, metaclass=ABCMeta):
    """
    An event base class.
    """
    def __init__(self, name, version="1", date=None, sender=None, corr_ids=None):
        date = date if date is not None else arrow.utcnow()
        corr_ids = corr_ids if corr_ids is not None else []

        self.name = name
        self.version = version
        self.date = date
        self.sender = sender
        self.corr_ids = corr_ids

    def equals(self, other, ignore_fields):
        ignore_fields = ignore_fields if ignore_fields is not None else []

        if isinstance(other, self.__class__):

            a = get_for_compare(self, ignore_fields)
            b = get_for_compare(other, ignore_fields)

            return a == b
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            a = copy.deepcopy(self.__dict__)
            b = copy.deepcopy(other.__dict__)
            a.pop('date')
            b.pop('date')
            return a == b
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @abstractmethod
    def get_serialized_payload(self):
        """
        Implemented by subclasses to provide the payload.
        """
        pass

    def serialize(self):
        obj = {
            'name': self.name,
            'version': self.version,
            'date': self.date.isoformat(),
            'sender': self.sender,
            'payload': self.get_serialized_payload(),
            'corr_ids': self.corr_ids,
        }
        return obj
