from pytz import timezone

from copy import deepcopy
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


class Scheduler:
    def __init__(self):
        jobstores = {"default": SQLAlchemyJobStore(url="sqlite:///movies.db")}

        self.scheduler = AsyncIOScheduler()

        self.scheduler.configure(
            jobstores=jobstores, timezone=timezone("America/Chicago")
        )

    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()

    def add_job(self, func, date, *args):
        self.scheduler.add_job(func, "date", run_date=date, args=deepcopy(args))
