from .command import BaseCommand


class PushwooshBaseClient(object):
    scheme = 'https'
    hostname = 'cp.pushwoosh.com'
    endpoint = 'json'
    version = '1.3'
    method = 'POST'

    debug = False

    def invoke(self, command):
        assert isinstance(command, BaseCommand), 'Command must be instance of BaseCommand'
