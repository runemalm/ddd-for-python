from ddd.domain.building_block import BuildingBlock


class Entity(BuildingBlock):
    def __init__(self, version):
        super(Entity, self).__init__(version=version)
