from abc import ABCMeta, abstractmethod


class SchedulerAdapter(object, metaclass=ABCMeta):
    def __init__(self, exec_func, log_service):
        super().__init__()
        self.exec_func = exec_func
        self.log_service = log_service

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass

    @abstractmethod
    async def add_cron_job(
        self,
        id,
        name,
        args,
        kwargs,
        crontab_expr,
        weekdays,
        hour,
        minute,
        second,
        start_date,
        end_date,
        timezone,
        coalesce=False,
        misfire_grace_time=(60 * 60),
        replace_existing=True,
    ):
        pass

    @abstractmethod
    async def add_date_job(
        self,
        id,
        name,
        args,
        kwargs,
        date,
        timezone,
        coalesce=False,
        misfire_grace_time=(60 * 60),
        replace_existing=True,
    ):
        pass

    @abstractmethod
    async def add_interval_job(
        self,
        id,
        name,
        args,
        kwargs,
        interval,
        days,
        hours,
        minutes,
        seconds,
        start_date,
        end_date,
        timezone,
        coalesce=False,
        misfire_grace_time=(60 * 60),
        replace_existing=True,
    ):
        pass

    @abstractmethod
    async def get_job(self, job_id):
        pass

    @abstractmethod
    async def remove_job(self, job_id, raises=False):
        pass
