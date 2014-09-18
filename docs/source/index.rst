.. _index:

=====================================
pypushwoosh: Pushwoosh Python Library
=====================================

Supported API Version: 1.3

Getting Started
---------------

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


Features
--------

At the moment, pypushwoosh supports:

* Message commands:

  * CreateMessageForApplicationCommand
  * CreateMessageForApplicationGroupCommand
  * CreateTargetedMessageCommand
  * CompileFilterCommand
  * DeleteMessageCommand

* Device commands:

  * RegisterDeviceCommand
  * SetTagsCommand
  * SetBadgeCommand
  * PushStatCommand
  * GetNearestZoneCommand

For targeted messages, supports:

  * ApplicationFilter and ApplicationGroupFilter filters
  * Tag filters: IntegerTagFilter, StringTagFilter, ListTagFilter, DateTagFilter, DaysTagFilter, BooleanTagFilter
  * Tags filters by application
  * Operations filters: UnionFilter, IntersectFilter, SubtractFilter


Additional Resources
--------------------
* :doc:`API Reference <ref/index>`
* `Remote API Guide`: https://www.pushwoosh.com/programming-push-notification/pushwoosh-push-notification-remote-api
* `Advanced Tags Guide`: https://www.pushwoosh.com/programming-push-notification/advanced-tags-guide


.. toctree::
   :hidden:
   :glob:

   ref/*

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
