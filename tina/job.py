"""
Interface for jobs
"""

import abc
import datetime


class Job(metaclass=abc.ABCMeta):

    def __init__(self):
        self._last_execution = None

    @property
    @abc.abstractmethod
    def interval(self) -> datetime.timedelta:
        raise NotImplementedError("interval")

    @property
    def name(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError("run")

    def __call__(self, *args, **kwargs):
        self.run()

    @property
    def last_execution(self):
        return self._last_execution

    @last_execution.setter
    def last_execution(self, now):
        self._last_execution = now
