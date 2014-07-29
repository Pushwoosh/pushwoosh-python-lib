pushwoosh-python-lib
====================

Pushwoosh Python Library

Supported API Version: 1.3

Typical usage often looks like this::

    #!/usr/bin/env python
    from pypushwoosh.client import PushwooshClient
    from pypushwoosh.command import CreateTargetedMessageCommand
    from pypushwoosh.filter import ApplicationFilter


    command = CreateTargetedMessageCommand()
    command.auth = 'AUTH_TOKEN'
    command.devices_filter = ApplicationFilter('APP-CODE')
    command.content = "Hello world!"

    client = PushwooshClient()
    print client.invoke(command)
   