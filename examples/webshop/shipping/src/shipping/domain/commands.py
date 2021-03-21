"""
The domain commands.
"""
from ddd.domain.command import Command


# Actions

class SendTrackingEmailCommand(Command):
    def __init__(
        self,
        shipment_id,
        token,
    ):
        super().__init__()
        self.shipment_id = shipment_id
        self.token = token
