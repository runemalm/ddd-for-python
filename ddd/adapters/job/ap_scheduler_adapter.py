from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.base import JobLookupError
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from ddd.adapters.job.exceptions import JobNotFound
from ddd.adapters.job.scheduler_adapter import SchedulerAdapter


class ApSchedulerAdapter(SchedulerAdapter):
    def __init__(self, dsn, exec_func, log_service):
        super().__init__(
            exec_func=exec_func,
            log_service=log_service
        )
        self.dsn = dsn

        self.scheduler = None

        self.create_scheduler()

    def create_scheduler(self):
        self.scheduler = AsyncIOScheduler()

        self.scheduler.configure(
            jobstores={
                'default': SQLAlchemyJobStore(url=self.dsn),
            },
            executors={
                'default': AsyncIOExecutor(),
            },
            job_defaults={
                'coalesce': False,
                'max_instances': 1,
                'misfire_grace_time': (60 * 60)
            },
            timezone="UTC",
        )

    async def start(self):
        self.scheduler.start()

    async def stop(self):
        self.scheduler.shutdown(wait=True)

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
        weekdays = weekdays if weekdays is not None else []

        trigger = None

        if crontab_expr is not None:
            trigger = \
                CronTrigger.from_crontab(
                    crontab_expr,
                    timezone=timezone,
                )
        else:
            trigger = \
                CronTrigger(
                    day_of_week=
                    ",".join(
                        [w[0:3].upper() for w in weekdays]
                    )
                    if len(weekdays) > 0
                    else None,
                    hour=hour,
                    minute=minute,
                    second=second,
                    start_date=start_date,
                    end_date=end_date,
                    timezone=timezone,
                )

        await self._add_job(
            id=id,
            name=name,
            func=self.exec_func,
            kwargs=kwargs,
            trigger=trigger,
            coalesce=coalesce,
            misfire_grace_time=misfire_grace_time,
            replace_existing=replace_existing,
        )

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
        raise NotImplementedError()

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
        raise NotImplementedError()

    async def get_job(self, job_id):
        return self.scheduler.get_job(job_id)

    async def remove_job(self, job_id, raises=False):
        try:
            self.scheduler.remove_job(job_id)
        except JobLookupError as e:
            if "No job by the id of" in str(e):
                self.log_service.error(
                    f"Tried to remove apscheduler job with ID '{job_id}' but "
                    f"it wasn't found. Ignoring but you should look this "
                    f"up since it should never happen."
                )
                if raises:
                    raise JobNotFound(job_id)
            else:
                raise

    async def remove_all_jobs(self):
        """
        Removes all scheduled jobs.
        """
        for job in self.scheduler.get_jobs():
            self.scheduler.remove_job(job.id)

    # Helpers

    async def _add_job(self, **kwargs):
        """
        Convenience method for adding a job.
        """
        self.scheduler.add_job(
            **kwargs
        )
