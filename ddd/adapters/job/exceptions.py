"""
The job adapter exceptions.
"""
class JobException(Exception):
    """
    Base class.
    This class must not be used directly.
    """
    def __init__(self, message):
        super().__init__(message)


class JobNotFound(JobException):
    def __init__(self, job_id):
        super().__init__(
            f"Couldn't find job with ID: '{job_id}'."
        )
        self.job_id = job_id
