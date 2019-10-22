# Test Server
import time
import pytest
from mock import Mock
from tina.job import Job
from tina.server import Server
from datetime import timedelta


class MockJob(Job):

    def __init__(self):
        super(MockJob, self).__init__()
        self.mock = Mock()

    @property
    def interval(self):
        return timedelta(seconds=1)

    def run(self):
        self.mock()


class TestServer:

    def test_register_job(self):
        """
        Test the correct registration of the job.
        Also tests that the job is executed the correct amount of times
        """

        server = Server()

        mock_job = MockJob()

        server.register_job(mock_job)

        server.run()

        time.sleep(2.5)

        assert mock_job.mock.call_count == 2

    def test_double_register_fails(self):
        """
        Test that registering the same job twice fails.
        """

        server = Server()

        mock_job = MockJob()

        server.register_job(mock_job)

        with pytest.raises(ValueError):
            server.register_job(mock_job)



