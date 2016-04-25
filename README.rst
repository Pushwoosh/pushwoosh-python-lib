pypushwoosh
===========

Pushwoosh Python Library

Supported API Version: 1.3

.. image:: https://travis-ci.org/Pushwoosh/pushwoosh-python-lib.svg?branch=master
    :target: https://travis-ci.org/Pushwoosh/pushwoosh-python-lib

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
  * GetTagsCommand
  * SetTagsCommand
  * SetBadgeCommand
  * PushStatCommand
  * GetNearestZoneCommand

For targeted messages, supports:

  * ApplicationFilter and ApplicationGroupFilter filters
  * Tag filters: IntegerTagFilter, StringTagFilter, ListTagFilter, DateTagFilter, DaysTagFilter, BooleanTagFilter
  * Tags filters by application
  * Operations filters: UnionFilter, IntersectFilter, SubtractFilter   


Installation
____________
   
Install via `pip`_:

::

    $ pip install pypushwoosh

Install from source:

::

    $ git clone git://github.com/Pushwoosh/pushwoosh-python-lib.git
    $ cd pushwoosh-python-lib
    $ python setup.py install

.. _pip: https://pip.pypa.io/en/stable/