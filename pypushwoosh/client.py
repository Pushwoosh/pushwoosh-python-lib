import json
import logging

from six.moves import http_client

from .base import PushwooshBaseClient


log = logging.getLogger('pypushwoosh.client.log')


class PushwooshClient(PushwooshBaseClient):
    """
    Implementation of the Pushwoosh API Client.
    """
    headers = {'User-Agent': 'PyPushwooshClient',
               'Content-Type': 'application/json',
               'Accept': 'application/json'}

    def __init__(self):
        PushwooshBaseClient.__init__(self)
        connection_class = http_client.HTTPSConnection if self.scheme == 'https' else http_client.HTTPConnection
        self.connection = connection_class(self.hostname)

    def __del__(self):
        self.connection.close()

    def path(self, command):
        return '/'.join(('', self.endpoint, self.version, command.command_name))

    def invoke(self, command):
        PushwooshBaseClient.invoke(self, command)

        if self.debug:
            log.debug('Client: %s' % self.__class__.__name__)
            log.debug('Command: %s' % command.render())
            log.debug('Request URL: %s://%s%s' % (self.scheme, self.hostname, self.path(command)))
            log.debug('Request method: %s' % self.method)
            log.debug('Request headers: %s' % self.headers)

        self.connection.request('POST', self.path(command), command.render(), self.headers)
        response = self.connection.getresponse()

        if self.debug:
            log.debug('Response version: %s' % response.version)
            log.debug('Response code: %s' % response.status)
            log.debug('Response phrase: %s' % response.reason)
            log.debug('Response headers: %s' % response.getheaders())

        body = response.read()
        return json.loads(body)
