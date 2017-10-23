import logging

import requests

from .base import PushwooshBaseClient


log = logging.getLogger('pypushwoosh.client.log')


class PushwooshClient(PushwooshBaseClient):
    """
    Implementation of the Pushwoosh API Client.
    """
    headers = {'User-Agent': 'PyPushwooshClient',
               'Content-Type': 'application/json',
               'Accept': 'application/json'}

    def __init__(self, timeout=None):
        PushwooshBaseClient.__init__(self)
        self.timeout = timeout

    def path(self, command):
        return '{}://{}/'.format(self.scheme, self.hostname) + '/'.join((self.endpoint, self.version,
                                                                         command.command_name))

    def invoke(self, command):
        PushwooshBaseClient.invoke(self, command)
        url = self.path(command)
        payload = command.render()

        if self.debug:
            log.debug('Client: %s' % self.__class__.__name__)
            log.debug('Command: %s' % payload)
            log.debug('Request URL: %s' % url)
            log.debug('Request method: %s' % self.method)
            log.debug('Request headers: %s' % self.headers)

        r = requests.post(url, data=payload, headers=self.headers, timeout=self.timeout)

        if self.debug:
            log.debug('Response version: %s' % r.raw.version)
            log.debug('Response code: %s' % r.status_code)
            log.debug('Response phrase: %s' % r.reason)
            log.debug('Response headers: %s' % r.headers)
            log.debug('Response payload: %s' % r.json())

        return r.json()
