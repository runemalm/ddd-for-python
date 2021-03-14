from ddd.domain.value_object import ValueObject


class EntityId(ValueObject):
    def __init__(self, identity, version="1"):
        super(EntityId, self).__init__(version=version)
        self.identity = str(identity)

    def __str__(self):
        return self.identity

    def __eq__(self, other):
        if not isinstance(other, EntityId):
            return self.identity == str(other)

        return self.identity == other.identity
