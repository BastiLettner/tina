"""
The server is the core controlling unit.
It registers jobs and runs the API.
"""
import time
from .api import TinaAPI
from .job import Job
from timeloop import Timeloop
from collections import namedtuple


JobContainer = namedtuple("JobContainer", "job, job_start_timestamp job_interval")


class Server(object):

    def __init__(self):

        self._tl = Timeloop()

        self._jobs = dict()

        self.api = TinaAPI(self)

    def run_api(self):
        self.api.start()

    @property
    def jobs(self):
        return self._jobs

    def register_job(self, job: Job) -> None:
        """
        Raises:
              ValueError: If job has already been registered
        """

        if self.job_exists(job):
            raise ValueError("The job {} has already been registered.".format(job.name))
        else:
            self._jobs[job.name] = JobContainer(job=job, job_start_timestamp=time.ctime(), job_interval=job.interval)

        interval = job.interval

        @self._tl.job(interval=interval)
        def wrapper() -> None:
            job.last_execution = time.ctime()
            job.run()

    def run(self) -> None:
        self._tl.start()

    def stop(self) -> None:
        self._tl.stop()

    def job_exists(self, job: Job) -> bool:
        if job.__class__.__name__ in self._jobs:
            return True
        else:
            return False

    def manual_trigger(self, job_name: str) -> bool:
        # blocking
        if job_name not in self.jobs:
            return False
        else:
            self.jobs[job_name].job.run()
            return True
