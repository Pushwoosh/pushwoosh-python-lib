import unittest
import json
import uuid

from pypushwoosh import client
from pypushwoosh import constants
from pypushwoosh.command import CreateTargetedMessageCommand, CreateMessageForApplicationCommand, \
    CreateMessageForApplicationGroupCommand, DeleteMessageCommand, CompileFilterCommand, RegisterDeviceCommand, \
    UnregisterDeviceCommand, SetBadgeCommand, SetTagsCommand, GetNearestZoneCommand, PushStatCommand
from pypushwoosh.filter import ApplicationFilter
from pypushwoosh.notification import Notification
from pypushwoosh.exceptions import PushwooshCommandException, PushwooshNotificationException

HTTP_200_OK = 200
STATUS_OK = 'OK'


class TestCreateMessageCommand(unittest.TestCase):

    def setUp(self):
        self.client = client.PushwooshClient()
        self.notification = Notification()
        self.notification.content = 'Hello world!'
        self.auth = 'test_auth'
        self.code = '0000-0000'

    def test_valid_create_by_application(self):
        expected_result = {
            'request': {
                'application': self.code,
                'auth': self.auth,
                'notifications': [
                    {
                        'content': 'Hello world!',
                        'send_date': 'now'
                    }
                ]
            }
        }
        self.command = CreateMessageForApplicationCommand(self.notification, application=self.code)
        self.command.auth = self.auth

        command_dict = json.loads(self.command.render())
        self.assertDictEqual(command_dict, expected_result)

    def test_valid_create_by_application_group(self):
        expected_result = {
            'request': {
                'applications_group': self.code,
                'auth': self.auth,
                'notifications': [
                    {
                        'content': 'Hello world!',
                        'send_date': 'now'
                    }
                ]
            }
        }
        self.command = CreateMessageForApplicationGroupCommand(self.notification, application_group=self.code)
        self.command.auth = self.auth

        command_dict = json.loads(self.command.render())
        self.assertDictEqual(command_dict, expected_result)

    def test_valid_create_by_user(self):
        users_list = ['user_1', 'user_2']
        expected_result = {
            'request': {
                'application': self.code,
                'auth': self.auth,
                'notifications': [
                    {
                        'content': 'Hello world!',
                        'send_date': 'now',
                        'users': users_list,
                    }
                ]
            }
        }

        self.notification.users = users_list
        self.command = CreateMessageForApplicationCommand(self.notification, application=self.code)
        self.command.auth = self.auth

        command_dict = json.loads(self.command.render())
        self.assertDictEqual(command_dict, expected_result)

    def test_create_message_without_application(self):
        self.command = CreateMessageForApplicationCommand(self.notification)
        self.command.auth = self.auth
        self.assertRaises(PushwooshCommandException, self.command.compile)

    def test_create_message_without_application_group(self):
        self.command = CreateMessageForApplicationGroupCommand(self.notification)
        self.command.auth = self.auth
        self.assertRaises(PushwooshCommandException, self.command.compile)


class TestCreateTargetedMessageCommand(unittest.TestCase):

    def setUp(self):
        self.code = '0000-0000'
        self.auth = 'test_auth'

        self.client = client.PushwooshClient()
        self.command = CreateTargetedMessageCommand()
        self.command.auth = self.auth
        self.command.content = "Hello world!"

    def test_valid_create(self):
        expected_result = {
            'request': {
                'devices_filter': 'A("%s")' % self.code,
                'auth': self.auth,
                'content': 'Hello world!',
                'send_date': 'now'
            }
        }

        self.command.devices_filter = ApplicationFilter(self.code)

        command_dict = json.loads(self.command.render())
        self.assertDictEqual(command_dict, expected_result)

    def test_create_without_device_filter(self):
            self.assertRaises(PushwooshNotificationException, self.command.compile)


class TestDeleteMessageCommand(unittest.TestCase):

    def setUp(self):
        self.client = client.PushwooshClient()
        self.command = DeleteMessageCommand()
        self.auth = 'Test auth'
        self.command.auth = self.auth

    def test_valid_delete(self):
        message_code = 'message_code'
        expected_result = {
            'request': {
                'message': message_code,
                'auth': self.auth
            }
        }
        self.command.message = message_code

        command_dict = json.loads(self.command.render())
        self.assertDictEqual(command_dict, expected_result)

    def test_delete_without_message(self):
        self.assertRaises(PushwooshCommandException, self.command.compile)


class TestCompileFilterCommand(unittest.TestCase):

    def setUp(self):
        self.client = client.PushwooshClient()
        self.command = CompileFilterCommand()
        self.code = '0000-0000'

    def test_valid_compile_filter(self):
        auth = 'test_auth'
        expected_result = {
            'request': {
                'devices_filter': 'A("%s")' % self.code,
                'auth': auth
            }
        }
        self.command.auth = auth
        self.command.devices_filter = ApplicationFilter(self.code)

        command_dict = json.loads(self.command.render())
        self.assertDictEqual(command_dict, expected_result)

    def test_invalid_auth(self):
        self.command.devices_filter = ApplicationFilter(self.code)
        self.assertRaises(PushwooshCommandException, self.command.render)


class TestDeviceCommands(unittest.TestCase):

    def setUp(self):
        self.client = client.PushwooshClient()
        self.auth = 'test_auth'
        self.hwid = str(uuid.uuid4())
        self.push_token = str(uuid.uuid4())
        self.app_code = '0000-0000'

    def test_valid_register_device(self):
        expected_result = {
            'request': {
                'push_token': self.push_token,
                'application': self.app_code,
                'hwid': self.hwid,
                'device_type': constants.PLATFORM_ANDROID
            }
        }
        command = RegisterDeviceCommand(self.app_code, self.hwid, constants.PLATFORM_ANDROID, self.push_token)

        command_dict = json.loads(command.render())
        self.assertDictEqual(command_dict, expected_result)

    def test_set_tag_command(self):
        testtag = {'testtag': 'test'}
        expected_result = {
            'request': {
                'application': self.app_code,
                'hwid': self.hwid,
                'tags': testtag
            }
        }
        command = SetTagsCommand(self.app_code, self.hwid, testtag)

        command_dict = json.loads(command.render())
        self.assertDictEqual(command_dict, expected_result)

    def test_set_badge_command(self):
        badge = 5
        expected_result = {
            'request': {
                'application': self.app_code,
                'hwid': self.hwid,
                'badges': badge
            }
        }
        command = SetBadgeCommand(self.app_code, self.hwid, badge)

        command_dict = json.loads(command.render())
        self.assertDictEqual(command_dict, expected_result)

    def test_push_stat_command(self):
        stat_hash = 'test_hash'
        expected_result = {
            'request': {
                'application': self.app_code,
                'hash': stat_hash,
                'hwid': self.hwid
            }
        }
        command = PushStatCommand(self.app_code, self.hwid, stat_hash)

        command_dict = json.loads(command.render())
        self.assertDictEqual(command_dict, expected_result)

    def test_get_nearest_zone_command(self):
        lat = ''
        lng = ''
        expected_result = {
            'request': {
                'lat': lat,
                'lng': lng,
                'application': self.app_code,
                'hwid': self.hwid
            }
        }
        command = GetNearestZoneCommand(self.app_code, self.hwid, lat, lng)

        command_dict = json.loads(command.render())
        self.assertDictEqual(command_dict, expected_result)

    def test_valid_unregister_device(self):
        expected_result = {
            'request': {
                'application': self.app_code,
                'hwid': self.hwid
            }
        }
        command = UnregisterDeviceCommand(self.app_code, self.hwid)

        command_dict = json.loads(command.render())
        self.assertDictEqual(command_dict, expected_result)
