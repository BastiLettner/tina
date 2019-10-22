# Test the tina api

import datetime
from tina.api import TinaAPI
from datetime import timedelta
from tina.job import Job
from mock import Mock
from tina.server import Server


class MockJob(Job):

    def __init__(self):
        super(MockJob, self).__init__()
        self.mock = Mock()

    @property
    def interval(self):
        return timedelta(seconds=60)

    def run(self):
        self.mock()


class TestTinaApi:

    def test_extract_next_execution_time(self):

        interval = datetime.timedelta(seconds=60)

        last_execution = 'Tue Oct 22 21:21:03 2019'

        next_execution = TinaAPI.extract_next_execution_time(last_execution=last_execution, interval=interval)

        assert next_execution == 'Tue Oct 22 21:22:03 2019'

    def test_get_jobs(self):

        mock_job = MockJob()

        server = Server()
        server.register_job(mock_job)

        api = TinaAPI(server=server)
        jobs = api.get_jobs_json()

        assert isinstance(jobs, list)
        assert len(jobs) == 1
        assert isinstance(jobs[0], dict)

        job = jobs[0]

        assert job['jobName'] == 'MockJob'
        assert job['jobIntervalSeconds'] == 60
        assert isinstance(job['jobStartTimeStamp'], str)
        assert isinstance(job['nextExecution'], str)
        assert job['lastExecution'] == ''
        t2 = datetime.datetime.strptime(job['nextExecution'], "%a %b %d %H:%M:%S %Y")
        t1 = datetime.datetime.strptime(job['jobStartTimeStamp'], "%a %b %d %H:%M:%S %Y")
        assert (t2 - t1).total_seconds() == 60


