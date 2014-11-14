import unittest

from pypushwoosh import constants, filter
from pypushwoosh.notification import Notification, DevicesFilterNotificationMixin
from pypushwoosh.filter import ApplicationFilter
from pypushwoosh.exceptions import PushwooshNotificationException

HTTP_200_OK = 200
STATUS_OK = 'OK'


class TestNotifications(unittest.TestCase):

    def setUp(self):
        self.notification = Notification()

    def notification_common(self):
        content = 'Hello World'
        send_date = '2014-05-13 00:00'
        ignore_user_timezone = 1
        page_id = 1
        link = 'http://test_link'
        data = '{"key": "value"}'

        expected_result = {
            'content': content,
            'send_date': send_date,
            'ignore_user_timezone': ignore_user_timezone,
            'page_id': page_id,
            'link': link,
            'minimize_link': constants.LINK_MINIMIZER_GOOGLE,
            'data': data
        }
        self.notification.content = content
        self.notification.send_date = send_date
        self.notification.ignore_user_timezone = ignore_user_timezone
        self.notification.page_id = page_id
        self.notification.link = link
        self.notification.data = data

        return expected_result

    def notification_filtered(self):
        platforms = [constants.PLATFORM_ANDROID, constants.PLATFORM_AMAZON]
        devices = ['test_push_device_token1', 'test_push_device_token2']
        conditions = str(filter.ApplicationFilter('0000-0000').union(ApplicationFilter('0000-0001')))

        expected_result = {
            'platforms': platforms,
            'devices': devices,
            'conditions': conditions
        }
        self.notification.platforms = platforms
        self.notification.devices = devices
        self.notification.conditions = conditions

        return expected_result

    def notification_ios(self):
        ios_badges = 5
        ios_sound = 'test.mp3'
        ios_ttl = 60 * 60 * 24
        apns_trim_content = True

        expected_result = {
            'ios_badges': ios_badges,
            'ios_sound': ios_sound,
            'ios_ttl': ios_ttl,
            'apns_trim_content': apns_trim_content

        }
        self.notification.ios_badges = ios_badges
        self.notification.ios_sound = ios_sound
        self.notification.ios_ttl = ios_ttl
        self.notification.apns_trim_content = apns_trim_content

        return expected_result

    def notification_android(self):
        android_sound = 'test.mp3'
        android_header = 'Test header'
        android_icon = 'icon in app'
        android_custom_icon = 'icon_url'
        android_banner = 'banner_url'
        android_gcm_ttl = 60 * 60 * 24

        expected_result = {
            'android_sound': android_sound,
            'android_header': android_header,
            'android_icon': android_icon,
            'android_custom_icon': android_custom_icon,
            'android_banner': android_banner,
            'android_gcm_ttl': android_gcm_ttl,
        }
        self.notification.android_sound = android_sound
        self.notification.android_header = android_header
        self.notification.android_icon = android_icon
        self.notification.android_custom_icon = android_custom_icon
        self.notification.android_banner = android_banner
        self.notification.android_gcm_ttl = android_gcm_ttl

        return expected_result

    def notification_wp(self):
        wp_type = 'Tile'
        wp_background = 'background_url'
        wp_backbackground = 'backbackground_url'
        wp_backtitle = 'Test title'
        wp_backcontent = 'Test content'
        wp_count = 23

        expected_result = {
            'wp_type': wp_type,
            'wp_background': wp_background,
            'wp_backbackground': wp_backbackground,
            'wp_backtitle': wp_backtitle,
            'wp_backcontent': wp_backcontent,
            'wp_count': wp_count,
        }
        self.notification.wp_type = wp_type
        self.notification.wp_background = wp_background
        self.notification.wp_backbackground = wp_backbackground
        self.notification.wp_backtitle = wp_backtitle
        self.notification.wp_backcontent = wp_backcontent
        self.notification.wp_count = wp_count

        return expected_result

    def notification_mac(self):
        mac_badges = 5
        mac_sound = 'test.mp3'
        mac_ttl = 60 * 60 * 24

        expected_result = {
            'mac_badges': mac_badges,
            'mac_sound': mac_sound,
            'mac_ttl': mac_ttl,
        }
        self.notification.mac_badges = mac_badges
        self.notification.mac_sound = mac_sound
        self.notification.mac_ttl = mac_ttl

        return expected_result

    def notification_wns(self):
        wns_content = {
            'en': 'Test en',
            'ru': 'Test ru'
        }
        wns_type = 'toast'
        wns_tag = 'test tag'

        expected_result = {
            'wns_content': wns_content,
            'wns_type': wns_type,
            'wns_tag': wns_tag,
        }
        self.notification.wns_content = wns_content
        self.notification.wns_type = wns_type
        self.notification.wns_tag = wns_tag

        return expected_result

    def notification_safari(self):
        safari_title = 'Test title'
        safari_action = 'Go!!!'
        safari_url_args = ['test', 'test.html']
        safari_ttl = 60 * 60 * 24

        expected_result = {
            'safari_title': safari_title,
            'safari_action': safari_action,
            'safari_url_args': safari_url_args,
            'safari_ttl': safari_ttl

        }
        self.notification.safari_title = safari_title
        self.notification.safari_action = safari_action
        self.notification.safari_url_args = safari_url_args
        self.notification.safari_ttl = safari_ttl

        return expected_result

    def notification_blackberry(self):
        blackberry_header = 'Test header'

        expected_result = {
            'blackberry_header': blackberry_header,

        }
        self.notification.blackberry_header = blackberry_header

        return expected_result

    def notification_amazon(self):
        adm_sound = 'test.mp3'
        adm_header = 'Test header'
        adm_icon = 'icon in app'
        adm_custom_icon = 'icon_url'
        adm_banner = 'banner_url'
        adm_ttl = 60 * 60 * 24

        expected_result = {
            'adm_sound': adm_sound,
            'adm_header': adm_header,
            'adm_icon': adm_icon,
            'adm_custom_icon': adm_custom_icon,
            'adm_banner': adm_banner,
            'adm_ttl': adm_ttl,
        }
        self.notification.adm_sound = adm_sound
        self.notification.adm_header = adm_header
        self.notification.adm_icon = adm_icon
        self.notification.adm_custom_icon = adm_custom_icon
        self.notification.adm_banner = adm_banner
        self.notification.adm_ttl = adm_ttl

        return expected_result

    def notification_chrome(self):
        chrome_header = 'Test header'
        chrome_icon = 'icon in app'
        chrome_ttl = 60 * 60 * 24

        expected_result = {
            'chrome_header': chrome_header,
            'chrome_icon': chrome_icon,
            'chrome_ttl': chrome_ttl,
        }
        self.notification.chrome_header = chrome_header
        self.notification.chrome_icon = chrome_icon
        self.notification.chrome_ttl = chrome_ttl

        return expected_result

    def test_full_notification(self):
        expected_result = dict()
        expected_result.update(self.notification_common())
        expected_result.update(self.notification_filtered())
        expected_result.update(self.notification_ios())
        expected_result.update(self.notification_android())
        expected_result.update(self.notification_wp())
        expected_result.update(self.notification_mac())
        expected_result.update(self.notification_wns())
        expected_result.update(self.notification_safari())
        expected_result.update(self.notification_amazon())
        expected_result.update(self.notification_blackberry())
        expected_result.update(self.notification_chrome())

        self.assertDictEqual(self.notification.render(), expected_result)

    def test_notification_common(self):
        expected_result = self.notification_common()
        self.assertDictEqual(self.notification.render(), expected_result)

    def test_notification_filtered(self):
        expected_result = {'content': None, 'send_date': 'now'}
        expected_result.update(self.notification_filtered())
        self.assertDictEqual(self.notification.render(), expected_result)

    def test_invalid_filtered_notification(self):
        notification = Notification()
        notification.filter = 'filter_name'
        notification.conditions = filter.ApplicationFilter('0000-0000')
        self.assertRaises(PushwooshNotificationException, notification.render)

    def test_notification_ios(self):
        expected_result = {'content': None, 'send_date': 'now'}
        expected_result.update(self.notification_ios())
        self.assertDictEqual(self.notification.render(), expected_result)

    def test_notification_android(self):
        expected_result = {'content': None, 'send_date': 'now'}
        expected_result.update(self.notification_android())
        self.assertDictEqual(self.notification.render(), expected_result)

    def test_notification_wp(self):
        expected_result = {'content': None, 'send_date': 'now'}
        expected_result.update(self.notification_wp())
        self.assertDictEqual(self.notification.render(), expected_result)

    def test_notification_mac(self):
        expected_result = {'content': None, 'send_date': 'now'}
        expected_result.update(self.notification_mac())
        self.assertDictEqual(self.notification.render(), expected_result)

    def test_notification_wns(self):
        expected_result = {'content': None, 'send_date': 'now'}
        expected_result.update(self.notification_wns())
        self.assertDictEqual(self.notification.render(), expected_result)

    def test_notification_safari(self):
        expected_result = {'content': None, 'send_date': 'now'}
        expected_result.update(self.notification_safari())
        self.assertDictEqual(self.notification.render(), expected_result)

    def test_notification_amazon(self):
        expected_result = {'content': None, 'send_date': 'now'}
        expected_result.update(self.notification_amazon())
        self.assertDictEqual(self.notification.render(), expected_result)

    def test_notification_blackberry(self):
        expected_result = {'content': None, 'send_date': 'now'}
        expected_result.update(self.notification_blackberry())
        self.assertDictEqual(self.notification.render(), expected_result)

    def test_notification_chrome(self):
        expected_result = {'content': None, 'send_date': 'now'}
        expected_result.update(self.notification_chrome())
        self.assertDictEqual(self.notification.render(), expected_result)


class TestNotificationsDevicesFilter(unittest.TestCase):

    def setUp(self):
        self.notification = DevicesFilterNotificationMixin()

    def test_invalid_devices_filter(self):
        self.assertRaises(PushwooshNotificationException, self.notification.devices_filter)
