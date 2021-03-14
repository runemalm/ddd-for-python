class DomainRegistry(object):
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if DomainRegistry.__instance is None:
            DomainRegistry()
        return DomainRegistry.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DomainRegistry.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DomainRegistry.__instance = self
            DomainRegistry.__instance.domain_publisher = None
            DomainRegistry.__instance.interchange_publisher = None
            DomainRegistry.__instance.task_db_conns = {}
            DomainRegistry.__instance.event_repository = None
            DomainRegistry.__instance.service = None
            DomainRegistry.__instance.log_service = None
