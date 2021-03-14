from ddd.infrastructure.infrastructure_service import InfrastructureService


class EmailService(InfrastructureService):
    """
    An email infrastructure service used to send emails.
    """
    def __init__(
        self,
        logger=None,
    ):
        super().__init__(logger=logger)

    async def send(
        self,
        from_,
        to_,
        subject,
        content,
    ):
        raise NotImplementedError()
