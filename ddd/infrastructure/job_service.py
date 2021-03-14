from ddd.infrastructure.infrastructure_service import InfrastructureService

from abc import ABCMeta, abstractmethod


class JobService(InfrastructureService, metaclass=ABCMeta):
    """
    A job service base class.
    """
    def __init__(
        self,
        scheduler_adapter,
        log_service,
    ):
        super().__init__(log_service=log_service)
        self.scheduler_adapter = scheduler_adapter

    async def start(self):
        await self.scheduler_adapter.start()

    async def stop(self):
        await self.scheduler_adapter.stop()

    # Schedule jobs

    async def add_cron_job(
        self,
        id,
        name,
        args,
        kwargs,
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
        return self.scheduler_adapter.add_cron_job(
            id=id,
            name=name,
            args=args,
            kwargs=kwargs,
            weekdays=weekdays,
            hour=hour,
            minute=minute,
            second=second,
            start_date=start_date.datetime,
            end_date=end_date.datetime,
            timezone=timezone,
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
        return self.scheduler_adapter.add_date_job(
            id=id,
            name=name,
            args=args,
            kwargs=kwargs,
            date=date.datetime,
            timezone=timezone,
            coalesce=coalesce,
            misfire_grace_time=misfire_grace_time,
            replace_existing=replace_existing,
        )

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
        return await self.scheduler_adapter.add_interval_job(
            id=id,
            name=name,
            args=args,
            kwargs=kwargs,
            interval=interval,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            start_date=start_date.datetime,
            end_date=end_date.datetime,
            timezone=timezone,
            coalesce=coalesce,
            misfire_grace_time=misfire_grace_time,
            replace_existing=replace_existing,
        )

    async def remove_job(self, job_id, raises=False):
        await self.scheduler_adapter.remove_job(
            job_id=job_id,
            raises=raises,
        )

    async def remove_all_jobs(self):
        await self.scheduler_adapter.remove_all_jobs()
