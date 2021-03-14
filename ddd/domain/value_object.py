from ddd.domain.building_block import BuildingBlock


class ValueObject(BuildingBlock):
    def __init__(self, version):
        super(ValueObject, self).__init__(version=version)
