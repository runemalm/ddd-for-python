from abc import abstractmethod


class JobAdapter(object):
    """
    The secondary 'scheduler' adapter schedules jobs.

    This is the primary 'jobs' adapter that is responsible for handling jobs
    when they are executed.
    """

    def __init__(self, log_service, token):
        super().__init__()
        self.set_log_service(log_service)
        self.set_token(token)

    # Setters

    @abstractmethod
    def set_log_service(self, log_service):
        pass

    @abstractmethod
    def set_token(self, token):
        pass

    @abstractmethod
    def set_service(self, service):
        pass

    @classmethod
    async def run_job(cls, **kwargs):
        """
        Does nothing since application logic (such as jobs)
        should be in your domain application service.

        Please override this class.
        """
        raise Exception(
            "The base class run_job method was called. "
            "This should never happen. You must have scheduled a job "
            "without having implemented a job adapter to handle the job. "
            "Please override the class if you need jobs."
        )
