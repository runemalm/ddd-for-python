import threading


class Transaction(object):
    def __init__(self):
        super(Transaction, self).__init__()

    async def __aenter__(self):
        return "dummy-transaction"

    async def __aexit__(self, type, value, traceback):
        pass


class Conn(object):
    def __init__(self):
        super(Conn, self).__init__()
        self.is_open = False

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def transaction(self):
        return Transaction()

    async def __aenter__(self):
        self.is_open = True

    async def __aexit__(self, type, value, traceback):
        self.is_open = False


class ConnectionHolder(object):
    def __init__(self):
        super(ConnectionHolder, self).__init__()

    async def __aenter__(self):
        self.conn = Conn()
        self.conn.open()
        return self.conn

    async def __aexit__(self, type, value, traceback):
        self.conn.close()


class MemoryPool(object):
    """
    The memory pool is used in the action decorator
    to create a "memory" transaction (for tests).
    """
    def __init__(self, max=80):
        super(MemoryPool, self).__init__()
        self.sem = threading.Semaphore(value=max)

    def acquire(self):
        self.sem.acquire()
        return ConnectionHolder()

    def release(self):
        self.sem.release()

    async def close(self):
        pass
