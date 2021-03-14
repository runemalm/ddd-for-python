from abc import ABCMeta

from ddd.adapters.message_reader import MessageReader


class EventListener(object, metaclass=ABCMeta):
    """
    An event listener.
    """
    def __init__(
        self,
        listens_to,
        action,
        command_creator,
        service=None,
        enabled=True,
    ):
        super(EventListener, self).__init__()

        self.listens_to_name = listens_to
        self.action = action
        self.service = service
        self.command_creator = command_creator
        self.enabled = enabled

    def listens_to(self, name):
        """
        Used to check if we listen to an event named 'name'.
        """
        if not self.listens_to_name:
            raise Exception("The 'listens_to_name' variable hasn't been set.")
        return name == self.listens_to_name

    async def handle(self, message):
        """
        Called when an event we are listening to is received.
        """
        if not self.enabled:
            return

        if self.command_creator is None:
            raise Exception(
                "Can't delegate event because command_creator is null.")

        self.message = message
        self.event = self.read_event()

        try:
            command = \
                self.command_creator(
                    event=self.event
                )
        except Exception as e:
            raise Exception(
                f"Couldn't create command using command "
                f"creator, error: {str(e)}"
            )
        action = getattr(self.service, self.action)

        await action(
            command=command,
            corr_ids=self.event.corr_ids,
        )

    def read_event(self):
        """
        Reads basic information of the event.
        """
        # Create reader
        self.reader = MessageReader(self.message)

        # Common properties
        self.type = self.reader.string_value('type')
        self.version = self.reader.string_value('version')
        self.name = self.reader.string_value('name')
        self.action_id = self.reader.string_value('action_id')
        self.corr_ids = self.reader.list_value('corr_ids')

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
