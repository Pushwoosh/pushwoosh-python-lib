from pypushwoosh.client import PushwooshClient
from pypushwoosh.command import CreateMessageForApplicationCommand
from pypushwoosh.notification import Notification

AUTH_TOKEN = 'AUTH_TOKEN'
APPLICATION_CODE = 'APP-CODE'

if __name__ == '__main__':
    notification = Notification()
    notification.content = 'Hello world!'
    notification.devices = [
        'PUSH_TOKEN_0',
        'PUSH_TOKEN_1',
    ]

    command = CreateMessageForApplicationCommand(notification, APPLICATION_CODE)
    command.auth = AUTH_TOKEN

    client = PushwooshClient()
    response = client.invoke(command)
