"""
The http adapter exceptions.
"""
class HttpException(Exception):
    """
    Base class for http adapter exceptions.
    This class must not be used directly. Throw one of it's subclasses instead.
    """
    def __init__(self, exception):
        super(HttpException, self).__init__()
        self.exception = exception


class NotReachableException(HttpException):
    def __init__(self, exception):
        super(NotReachableException, self).__init__(exception=exception)
