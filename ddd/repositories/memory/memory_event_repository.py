class MemoryEventRepository(object):
    def __init__(self):
        super(MemoryEventRepository, self).__init__()
        self.events = {
            'domain': {},
            'integration': {},
        }

    async def delete_all(self, action_id, event_type):
        self.events[event_type].pop(action_id, None)

    async def get_unpublished(self, action_id, event_type):
        if action_id in self.events[event_type]:
            return self.events[event_type][action_id]
        return []

    async def save_all(self, action_id, events, event_type):
        self.events[event_type][action_id] = events
