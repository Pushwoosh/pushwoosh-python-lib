import httplib
import json
import sys
from pprint import pformat

from pypushwoosh.base import PushwooshBaseClient


def _debug_request(client, command):
    print >> sys.stderr, 'Client:', client.__class__.__name__
    print >> sys.stderr, 'Command:', command.render()

    print >> sys.stderr, 'Request URL: %s://%s%s' % (client.scheme, client.hostname, client.path(command))
    print >> sys.stderr, 'Request method:', client.method
    print >> sys.stderr, 'Request headers:'
    print >> sys.stderr, pformat(client.headers)


def _debug_response(response):
    print >> sys.stderr, 'Response version:', response.version
    print >> sys.stderr, 'Response code:', response.status
    print >> sys.stderr, 'Response phrase:', response.reason
    print >> sys.stderr, 'Response headers:'
    print >> sys.stderr, pformat(response.getheaders())


class PushwooshClient(PushwooshBaseClient):
    headers = {'User-Agent': 'PyPushwooshClient',
               'Content-Type': 'application/json',
               'Accept': 'application/json'}

    def __init__(self):
        PushwooshBaseClient.__init__(self)
        connection_class = httplib.HTTPSConnection if self.scheme == 'https' else httplib.HTTPConnection
        self.connection = connection_class(self.hostname)

    def __del__(self):
        self.connection.close()

    def path(self, command):
        return '/'.join(('', self.endpoint, self.version, command.command_name))

    def invoke(self, command):
        PushwooshBaseClient.invoke(self, command)

        if self.debug:
            _debug_request(self, command)

        self.connection.request('POST', self.path(command), command.render(), self.headers)
        response = self.connection.getresponse()

        if self.debug:
            _debug_response(response)

        body = response.read()
        return json.loads(body)

