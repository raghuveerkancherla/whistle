import six
from abc import ABCMeta, abstractproperty, abstractmethod


class Handler(six.with_metaclass(ABCMeta)):

    @abstractproperty
    def name(self):
        pass

    @abstractmethod
    def handle_request(self, request):
        pass

    @abstractmethod
    def handle_response(self, response):
        pass
