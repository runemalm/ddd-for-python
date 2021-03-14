from ddd.domain.entity import Entity


class Aggregate(Entity):
    def __init__(self, version):
        super(Aggregate, self).__init__(version=version)
