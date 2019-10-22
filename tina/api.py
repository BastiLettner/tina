"""
This file contains a small API for the Tina Server which provides information about registered jobs
"""

import flask
import threading
import datetime
from flask import jsonify, request


class TinaAPI(threading.Thread):

    app = None
    api_root = '/api/v1/tina'

    def __init__(self, server, auth=None):

        super(TinaAPI, self).__init__()
        self.server = server
        self.app = flask.Flask(__name__)
        self.register_routes()
        self.auth = auth.authenticate if auth is not None else lambda data: True

    def run(self) -> None:
        self.app.run()

    def register_routes(self) -> None:

        @self.app.route(self.api_root, methods=['GET'])
        def list_jobs():

            data = request.json
            if not self.auth(data):
                return jsonify({'message': 'Not authenticated'}), 401

            jobs = self.get_jobs_json()

            return jsonify(jobs), 200

        @self.app.route(self.api_root + '/<jobName>', methods=['POST'])
        def trigger_job(jobName):

            data = request.json
            if not self.auth(data):
                return jsonify({'message': 'Not authenticated'}), 401

            success = self.server.manual_trigger(job_name=jobName)
            if success:
                return jsonify({'message': 'Success'})
            else:
                return jsonify({'message': 'job with name {} does not exist.'.format(data['jobName'])})

    def get_jobs_json(self) -> list:

        jobs = []

        for job_name, job_container in self.server.jobs.items():

            last_execution = job_container.job.last_execution
            if last_execution is None:
                last_execution = ""

            jobs.append({
                "jobName": job_name,
                "jobIntervalSeconds": int(job_container.job_interval.total_seconds()),
                "jobStartTimeStamp": job_container.job_start_timestamp,
                "lastExecution": last_execution,
                "nextExecution": TinaAPI.extract_next_execution_time(
                    last_execution if last_execution != '' else job_container.job_start_timestamp,
                    job_container.job.interval
                )
            })

        return jobs

    @staticmethod
    def extract_next_execution_time(last_execution: str, interval: datetime.timedelta) -> str:
        """
        Returns the timestamp for the next execution.
        Formatted as "%a %b %d %H:%M:%S %Y", e.g. Tue Oct 22 21:58:51 2019
        """
        last_execution_formatted = datetime.datetime.strptime(last_execution, "%a %b %d %H:%M:%S %Y")
        next_execution = last_execution_formatted + interval
        next_execution_formatted = datetime.datetime.strftime(next_execution, "%a %b %d %H:%M:%S %Y")
        return next_execution_formatted
