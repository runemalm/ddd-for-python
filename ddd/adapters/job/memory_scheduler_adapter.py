from ddd.adapters.job.scheduler_adapter import SchedulerAdapter


class MemorySchedulerAdapter(SchedulerAdapter):
    def __init__(self, exec_func, log_service):
        super().__init__(
            exec_func=exec_func,
            log_service=log_service
        )

        self.jobs = {
            'cron': {},
            'date': {},
            'interval': {},
        }

    async def start(self):
        pass

    async def stop(self):
        pass

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
        self.jobs['cron'][id] = {
            'id': id,
            'name': name,
            'args': args,
            'kwargs': kwargs,
            'crontab_expr': crontab_expr,
            'weekdays': weekdays,
            'hour': hour,
            'minute': minute,
            'second': second,
            'start_date': start_date,
            'end_date': end_date,
            'timezone': timezone,
            'coalesce': coalesce,
            'misfire_grace_time': misfire_grace_time,
        }

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
        self.jobs['date'][id] = {
            'id': id,
            'name': name,
            'args': args,
            'kwargs': kwargs,
            'date': date,
            'timezone': timezone,
            'coalesce': coalesce,
            'misfire_grace_time': misfire_grace_time,
        }

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
        self.jobs['interval'][id] = {
            'id': id,
            'name': name,
            'args': args,
            'kwargs': kwargs,
            'interval': interval,
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'start_date': start_date,
            'end_date': end_date,
            'timezone': timezone,
            'coalesce': coalesce,
            'misfire_grace_time': misfire_grace_time,
        }

    async def get_job(self, job_id):
        for i, j in self.jobs['cron'].items():
            if i == job_id:
                return j

        for i, j in self.jobs['date'].items():
            if i == job_id:
                return j

        for i, j in self.jobs['interval'].items():
            if i == job_id:
                return j

    async def remove_job(self, job_id, raises=False):
        self.jobs['cron'] = {
            i: j
            for i, j in self.jobs['cron'].items()
            if i != job_id
        }

        self.jobs['date'] = {
            i: j
            for i, j in self.jobs['date'].items()
            if i != job_id
        }

        self.jobs['interval'] = {
            i: j
            for i, j in self.jobs['interval'].items()
            if i != job_id
        }
