"""
Interface for auth
"""
import abc


class Auth(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def authenticate(self, data) -> bool:
        raise NotImplementedError
