# Tina

Server for background processing jobs.


# Functionality

- interface for implementing (recurring) jobs
- minimal api (GET for configured jobs and POST for trigger)
- interface for auth (API)

# API

- /api/v1/tina (GET): Returns list containing information of each job as json
- /api/v1/tina/<jobName> (POST): trigger job manually. Does not affect recurring scheduling

# DEMO
Runs hello world every five seconds

```python
# Small hello world example

import datetime
from tina.job import Job
from tina.server import Server

# Job interface
# Need to implement .interval and .run()
class HelloWorldJob(Job):

    @property
    def interval(self):
        return datetime.timedelta(seconds=5)

    def run(self):
        print("Hello, World!")


def main():

    server = Server()
    server.register_job(HelloWorldJob())
    server.run()  # non-blocking
    server.run_api()  # api needs to be started separately
    while True:
        pass


if __name__ == '__main__':
    main()
```

