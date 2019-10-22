# Small hello world example

import datetime
from tina.job import Job
from tina.server import Server


class HelloWorldJob(Job):

    @property
    def interval(self):
        return datetime.timedelta(seconds=5)

    def run(self):
        print("Hello, World!")


def main():

    server = Server()
    server.register_job(HelloWorldJob())
    server.run()
    server.run_api()
    while True:
        pass


if __name__ == '__main__':
    main()