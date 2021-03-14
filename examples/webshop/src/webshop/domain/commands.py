"""
The domain commands.
"""
from ddd.domain.command import Command


# Actions

class SendWelcomeEmailCommand(Command):
    def __init__(
        self,
        customer_id,
        token,
    ):
        super().__init__()
        self.customer_id = customer_id
        self.token = token
