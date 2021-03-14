class EntityIdTranslator(object):
    def __init__(self, entity_id):
        super().__init__()
        self.entity_id = entity_id

    @classmethod
    def from_domain(cls, identity, entity_class):
        entity_id = entity_class(identity=identity)
        return entity_id
