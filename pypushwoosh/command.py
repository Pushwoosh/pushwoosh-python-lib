import json

from six import add_metaclass

from .notification import Notification, DevicesFilterNotificationMixin, BaseNotification, \
    BaseNotificationMeta, IOSNotificationMixin, AndroidNotificationMixin, WindowsPhoneNotificationMixin, \
    OSXNotificationMixin, Windows8NotificationMixin, SafariNotificationMixin, AmazonNotificationMixin, \
    BlackBerryNotificationMixin, CommonNotificationMixin, ChromeNotificationMixin
from .utils import render_attrs
from .exceptions import PushwooshCommandException


class BaseCommand(object):
    command_name = None

    def __init__(self):
        self._command = {}
        self._command_compiled = False

    def compile(self):
        self._command = {'request': self._command}
        self._command_compiled = True

    def render(self):
        if not self._command_compiled:
            self.compile()
        return json.dumps(self._command, default=str)


class BaseAuthCommand(BaseCommand):
    """
    Command with auth attribute

    Attributes:
        auth (str): Required. API access token from the Pushwoosh control panel (create this token
        at https://cp.pushwoosh.com/api_access)
    """
    def __init__(self):
        BaseCommand.__init__(self)
        self.auth = None

    def compile(self):
        if self.auth is None:
            raise PushwooshCommandException('auth is required')

        self._command['auth'] = self.auth
        BaseCommand.compile(self)


class BaseCreateMessageCommand(BaseAuthCommand):
    """
    Creates new push notification command

    Attributes:
        application (str): Optional. Pushwoosh application ID where you send the message to (cannot be used together
        with "applications_group")

        application_group (str): Optional. Pushwoosh Application group code (cannot be used together with "application")

        notifications (BaseNotification | list of BaseNotification): Required.
    """
    command_name = 'createMessage'

    def __init__(self, notifications):
        BaseAuthCommand.__init__(self)

        if isinstance(notifications, Notification):
            notifications = [notifications]

        assert isinstance(notifications, list)
        for notification in notifications:
            assert isinstance(notification, Notification)

        self.notifications = notifications

    def _set_recipient(self):
        pass

    def compile(self):
        self._set_recipient()

        notifications = []
        for notification in self.notifications:
            notifications.append(notification.render())
        self._command['notifications'] = notifications

        BaseAuthCommand.compile(self)


class CreateMessageForApplicationCommand(BaseCreateMessageCommand):

    def __init__(self, notifications, application=None):
        super(CreateMessageForApplicationCommand, self).__init__(notifications)
        self.application = application

    def _set_recipient(self):
        if self.application is None:
            raise PushwooshCommandException('application is required')

        self._command['application'] = self.application


class CreateMessageForApplicationGroupCommand(BaseCreateMessageCommand):

    def __init__(self, notifications, application_group=None):
        super(CreateMessageForApplicationGroupCommand, self).__init__(notifications)
        self.application_group = application_group

    def _set_recipient(self):
        if self.application_group is None:
            raise PushwooshCommandException('application_group is required')
        self._command['applications_group'] = self.application_group


class DeleteMessageCommand(BaseAuthCommand):
    """
    Deletes the message command

    Attributes:
        message (str): Required. Message code obtained in createMessage
    """
    command_name = 'deleteMessage'

    def __init__(self, message=None):
        BaseAuthCommand.__init__(self)
        self.message = message

    def compile(self):
        if self.message is None:
            raise PushwooshCommandException('message is required')

        render_attrs(self, self._command, ['message'])
        BaseAuthCommand.compile(self)


@add_metaclass(BaseNotificationMeta)
class CreateTargetedMessageCommand(BaseAuthCommand,
                                   BaseNotification,
                                   IOSNotificationMixin,
                                   AndroidNotificationMixin,
                                   WindowsPhoneNotificationMixin,
                                   OSXNotificationMixin,
                                   Windows8NotificationMixin,
                                   SafariNotificationMixin,
                                   AmazonNotificationMixin,
                                   BlackBerryNotificationMixin,
                                   ChromeNotificationMixin,
                                   DevicesFilterNotificationMixin,
                                   CommonNotificationMixin):
    """
    Creates new push notification command (from Advanced Tags Guide)
    """
    command_name = 'createTargetedMessage'

    def __init__(self):
        BaseAuthCommand.__init__(self)
        BaseNotification.__init__(self)

    def compile(self):
        self._command.update(BaseNotification.render(self))
        BaseAuthCommand.compile(self)


@add_metaclass(BaseNotificationMeta)
class CompileFilterCommand(BaseAuthCommand, BaseNotification, DevicesFilterNotificationMixin):
    """
    Compiling filters and dry-run command (from Advanced Tags Guide)
    """
    command_name = 'compileFilter'

    def __init__(self):
        BaseAuthCommand.__init__(self)
        BaseNotification.__init__(self)

    def compile(self):
        self._command.update(BaseNotification.render(self))
        BaseAuthCommand.compile(self)


class BaseDeviceCommand(BaseCommand):
    """
    Base device command.

    Attributes:
        application (str): Required. Pushwoosh application ID where you send the message to

        hwid (str): Required. Unique string to identify the device (Please note that accessing UDID on iOS is
        deprecated and not allowed, one of the alternative ways now is to use MAC address or IdentifierForVendors)
    """
    def __init__(self, application, hwid):
        BaseCommand.__init__(self)
        self.application = application
        self.hwid = hwid

    def compile(self):
        render_attrs(self, self._command, ['application', 'hwid'])
        BaseCommand.compile(self)


class RegisterDeviceCommand(BaseDeviceCommand):
    """
    Registers device for the application

    Attributes:
        device_type (str): Required. Device type. Please see PLATFORM_* constants

        push_token (str): Required. Push token for the device

        language (str): Optional. Language locale of the device

        timezone (str): Optional. Timezone offset in seconds for the device
    """
    command_name = 'registerDevice'

    def __init__(self, application, hwid, device_type, push_token, language=None, timezone=None):
        BaseDeviceCommand.__init__(self, application, hwid)
        self.device_type = device_type
        self.push_token = push_token
        self.language = language
        self.timezone = timezone

    def compile(self):
        render_attrs(self, self._command, ['device_type', 'push_token', 'language', 'timezone'])
        BaseDeviceCommand.compile(self)


class UnregisterDeviceCommand(BaseDeviceCommand):
    """
    Remove device from the application
    """
    command_name = 'unregisterDevice'


class SetTagsCommand(BaseDeviceCommand):
    """
    Registers device for the application

    Attributes:
        tags (dict of tags): Required. tags to set
    """
    command_name = 'setTags'

    def __init__(self, application, hwid, tags):
        BaseDeviceCommand.__init__(self, application, hwid)
        self.tags = tags

    def compile(self):
        render_attrs(self, self._command, ['tags'])
        BaseDeviceCommand.compile(self)


class SetBadgeCommand(BaseDeviceCommand):
    """
    Set current badge value for the device to let auto-incrementing badges work properly

    Attributes:
        badges (int): Required. Current badge on the application to use with auto-incrementing badges
    """
    command_name = 'setBadge'

    def __init__(self, application, hwid, badges):
        BaseDeviceCommand.__init__(self, application, hwid)
        self.badges = badges

    def compile(self):
        render_attrs(self, self._command, ['badges'])
        BaseDeviceCommand.compile(self)


class PushStatCommand(BaseDeviceCommand):
    """
    Register push open event

    Attributes:
        hash (str): Required. Hash tag received in push notification
    """
    command_name = 'pushStat'

    def __init__(self, application, hwid, hash):
        BaseDeviceCommand.__init__(self, application, hwid)
        self.hash = hash

    def compile(self):
        render_attrs(self, self._command, ['hash'])
        BaseDeviceCommand.compile(self)


class GetNearestZoneCommand(BaseDeviceCommand):
    """
    Records device location for geo push notifications

    Attributes:
        lat (float): Required. Latitude of the device

        lng (float): Required. Longitude of the device
    """
    command_name = 'getNearestZone'

    def __init__(self, application, hwid, lat, lng):
        BaseDeviceCommand.__init__(self, application, hwid)
        self.lat = lat
        self.lng = lng

    def compile(self):
        render_attrs(self, self._command, ['lat', 'lng'])
        BaseDeviceCommand.compile(self)
