# coding=utf-8
from six import string_types, add_metaclass

from . import constants
from .filter import BaseFilter
from .utils import render_attrs
from .exceptions import PushwooshNotificationException


class BaseNotificationMixin(object):
    pass


class BaseNotification(object):
    _mixed = tuple()

    def __init__(self):
        for klass in self._mixed:
            klass.__init__(self)

    def render(self):
        result = {}
        for klass in self._mixed:
            ret = klass.render(self)
            result.update(ret)
        return result


class BaseNotificationMeta(type):
    def __new__(mcs, name, bases, dct):
        _mixed = set(dct.get('_mixed', tuple()))
        for klass in bases:
            if issubclass(klass, BaseNotificationMixin) and not issubclass(klass, BaseNotification):
                _mixed.add(klass)
            elif issubclass(klass, BaseNotification):
                _mixed.update(getattr(klass, '_mixed', tuple()))
        dct['_mixed'] = tuple(_mixed)
        return type.__new__(mcs, name, bases, dct)


class CommonNotificationMixin(BaseNotificationMixin):
    """
    Describe base notification attributes such as content, send_date, link, page_id etc.

    Attributes:
        send_date (str): Required. Time when need to send notification (YYYY-MM-DD HH:mm or 'now').

        content (dict or str): Required. Notification text or dictionary of language-text map.

        ignore_user_timezone (bool): Optional. Ignore device time zone when sending message. Default False.

        page_id (int): Optional. Page number for rich push.

        link (str): Optional. Link

        minimize_link (int): Optional. Minimizer type. See constant.MINIMIZER_* for more information. Default "goo.gl"

        data (dict): Optional. Custom data will be passed to device with notification.
    """

    def __init__(self):
        self.send_date = constants.SEND_DATE_NOW
        self.ignore_user_timezone = None
        self.content = None
        self.page_id = None
        self.link = None
        self.minimize_link = constants.LINK_MINIMIZER_GOOGLE
        self.data = None

    def render(self):
        result = {
            'send_date': self.send_date,
            'content': self.content,
        }
        render_attrs(self, result, ('ignore_user_timezone', 'page_id', 'link', 'data'))

        if 'link' in result:
            result['minimize_link'] = self.minimize_link

        return result


class FilteredNotificationMixin(BaseNotificationMixin):
    """
    Filter attributes mixin to notification.

    Attributes:
        platform (list of int): Optional.

        devices (list of str): Optional.

        filter (str): Optional.

        conditions (list of conditions): Optional.

    """

#   TODO: better describe this

    def __init__(self):
        self.platforms = None
        self.devices = None
        self.filter = None
        self.conditions = None

    def render(self):
        if self.filter is not None and self.conditions is not None:
            raise PushwooshNotificationException('filter and conditions is mutually exclusive options')

        result = {}
        render_attrs(self, result, ('platforms', 'devices', 'filter', 'conditions'))
        return result


class DevicesFilterNotificationMixin(BaseNotificationMixin):
    """
    Devices Filter mixin uses in CreateTargetedMessageCommand

    Attributes:
        devices_filter (BaseFilter|str): Required.
    """

#   TODO: better describe this

    def __init__(self):
        self._devices_filter = None

    @property
    def devices_filter(self):
        return self._devices_filter

    @devices_filter.setter
    def devices_filter(self, filter):
        if not (isinstance(filter, BaseFilter) or isinstance(filter, string_types)):
            raise PushwooshNotificationException('Must be BaseFilter or string.')
        self._devices_filter = filter

    def render(self):
        if self.devices_filter is None:
            raise PushwooshNotificationException('devices_filter is required')
        return {'devices_filter': self.devices_filter}


class IOSNotificationMixin(BaseNotificationMixin):
    """
    iOS platform related attributes mixin to notification.

    Attributes:
        ios_badges (int): Optional. This value will be sent to ALL devices given in "devices"

        ios_sound (str): Optional. Sound file name in the main bundle of application

        ios_ttl (int): Optional. Time to live parameter - the maximum lifespan of a message in seconds

        ios_category_id (int): Optional. iOS8 category id from pushwoosh control panel

        ios_root_params (dict): Optional. Root level parameters to the aps dictionary.

        apns_trim_content (bool): Optional. Trims the exceeding content strings with ellipsis
    """

    def __init__(self):
        self.ios_badges = None
        self.ios_sound = None
        self.ios_ttl = None
        self.ios_category_id = None
        self.ios_root_params = None
        self.apns_trim_content = None

    def render(self):
        result = {}
        render_attrs(self, result, ('ios_badges', 'ios_sound', 'ios_ttl', 'ios_root_params', 'apns_trim_content'))
        return result


class AndroidNotificationMixin(BaseNotificationMixin):
    """
    Android platform related attributes mixin to notification.

    Attributes:
        android_root_params (dict): Optional. Root level parameters for the android payload recipients.

        android_sound (str): Optional. Sound file name in the "res/raw" folder, do not include the extension

        android_header (str): Optional. Android notification header

        android_icon (str): Optional.

        android_custom_icon (str): Optional. Full path URL to the image file

        android_banner (str): Optional. Full path URL to the image file

        android_gcm_ttl (int): Optional. Time to live parameter - the maximum lifespan of a message in seconds
    """

    def __init__(self):
        self.android_root_params = None
        self.android_sound = None
        self.android_header = None
        self.android_icon = None
        self.android_custom_icon = None
        self.android_banner = None
        self.android_gcm_ttl = None

    def render(self):
        result = {}
        render_attrs(self, result, ('android_root_params', 'android_sound', 'android_header', 'android_icon',
                                    'android_custom_icon', 'android_banner', 'android_gcm_ttl'))
        return result


class WindowsPhoneNotificationMixin(BaseNotificationMixin):
    """
    Windows Phone platform related attributes mixin to notification.

    Attributes:
        wp_type (str): Optional. Windows Phone notification type. 'Tile' or 'Toast'. Raw notifications are not supported

        wp_background (str): Optional. Tile image

        wp_backbackground (str): Optional. Back tile image

        wp_backtitle (str): Optional. Back tile title

        wp_backcontent (str): Optional. Back tile content

        wp_count (int): Optional. Badge for Windows Phone notification
    """

    def __init__(self):
        self.wp_type = None
        self.wp_background = None
        self.wp_backbackground = None
        self.wp_backtitle = None
        self.wp_backcontent = None
        self.wp_count = None

    def render(self):
        result = {}
        render_attrs(self, result, ('wp_type', 'wp_background', 'wp_backbackground', 'wp_backtitle', 'wp_count', 'wp_backcontent'))
        return result


class OSXNotificationMixin(BaseNotificationMixin):
    """
    Mac OS X platform related attributes mixin to notification.

    Attributes:
        mac_badges (int): Optional.

        mac_sound (str): Optional. Sound file name in the main bundle of application

        mac_root_params (dict): Optional. Root level parameters to the aps dictionary.

        mac_ttl (int): Optional. Time to live parameter - the maximum lifespan of a message in seconds
    """

    def __init__(self):
        self.mac_badges = None
        self.mac_sound = None
        self.mac_root_params = None
        self.mac_ttl = None

    def render(self):
        result = {}
        render_attrs(self, result, ('mac_badges', 'mac_sound', 'mac_root_params', 'mac_ttl'))
        return result


class Windows8NotificationMixin(BaseNotificationMixin):
    """
    WNS platform related attributes mixin to notification.

    Attributes:
        wns_content (dict): Optional. Content (XML or raw) of notification encoded in MIME's base64 in form of
        Object( language1: 'content1', language2: 'content2' ) OR String

        wns_type (str): Optional. 'Tile' | 'Toast' | 'Badge' | 'Raw'

        wns_tag (str): Optional. Used in the replacement policy of the Tile. An alphanumeric string of no more than
        16 characters.
    """

    def __init__(self):
        self.wns_content = None
        self.wns_type = None
        self.wns_tag = None

    def render(self):
        result = {}
        render_attrs(self, result, ('wns_content', 'wns_type', 'wns_tag'))
        return result


class SafariNotificationMixin(BaseNotificationMixin):
    """
    Safari platform related attributes mixin to notification.

    Attributes:
        safari_title (str): Optional.

        safari_action (str): Optional.

        safari_url_args (list of str): Optional.

        safari_ttl (int): Optional.
    """

#   TODO: better describe this

    def __init__(self):
        self.safari_title = None
        self.safari_action = None
        self.safari_url_args = None
        self.safari_ttl = None

    def render(self):
        result = {}
        render_attrs(self, result, ('safari_title', 'safari_action', 'safari_url_args', 'safari_ttl'))
        return result


class AmazonNotificationMixin(BaseNotificationMixin):
    """
    Amazon platform related attributes mixin to notification.

    Attributes:
        adm_root_params (dict): Optional.

        adm_sound (str): Optional.

        adm_header (str): Optional.

        adm_icon (str): Optional.

        adm_custom_icon (str): Optional.

        adm_banner (str): Optional.

        adm_ttl (int): Optional.
    """

#   TODO: better describe this

    def __init__(self):
        self.adm_root_params = None
        self.adm_sound = None
        self.adm_header = None
        self.adm_icon = None
        self.adm_custom_icon = None
        self.adm_banner = None
        self.adm_ttl = None

    def render(self):
        result = {}
        render_attrs(self, result, ('adm_root_params', 'adm_sound', 'adm_header', 'adm_icon', 'adm_custom_icon',
                                    'adm_banner', 'adm_ttl'))
        return result


class BlackBerryNotificationMixin(BaseNotificationMixin):
    """
    BlackBerry platform related attributes mixin to notification.

    Attributes:
        blackberry_header (str): Optional.
    """

#   TODO: better describe this

    def __init__(self):
        self.blackberry_header = None

    def render(self):
        result = {}
        render_attrs(self, result, ('blackberry_header',))
        return result


class ChromeNotificationMixin(BaseNotificationMixin):
    """
   Chrome platform related attributes mixin to notification.

    Attributes:
        chrome_header (str): Optional
        chrome_icon (str):  Optional
        chrome_gcm_ttl (int): Optional
    """

#   TODO: better describe this

    def __init__(self):
        self.chrome_header = None
        self.chrome_icon = None
        self.chrome_ttl = None

    def render(self):
        result = {}
        render_attrs(self, result, ('chrome_header', 'chrome_icon', 'chrome_ttl',))
        return result


@add_metaclass(BaseNotificationMeta)
class Notification(BaseNotification,
                   IOSNotificationMixin,
                   AndroidNotificationMixin,
                   WindowsPhoneNotificationMixin,
                   OSXNotificationMixin,
                   Windows8NotificationMixin,
                   SafariNotificationMixin,
                   AmazonNotificationMixin,
                   BlackBerryNotificationMixin,
                   ChromeNotificationMixin,
                   FilteredNotificationMixin,
                   CommonNotificationMixin):
    """
    Pushwoosh notification. Includes all supported platforms mixins. Renders notification to dict.
    """
