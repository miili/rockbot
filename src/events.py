#!/usr/bin/env python3
import logging
logger = logging.getLogger('rockbot.events')

class AttrDict(dict):
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value


class Event(object):
    event = 'prototype'

    def __init__(self, event):
        self._ev = event
        if event['event'] != self.event:
            raise TypeError('Wrong event string %s for class %s'
                            % (event['event'], self.__class__.__name__))

        self.broadcast = AttrDict(**event['broadcast'])
        self.data = AttrDict(**event['data'])
        self.seq = int(event['seq'])
        # print('Initiated a %s' % self.__class__.__name__)


class HelloEvent(Event):
    event = 'hello'

    def __init__(self, event):
        Event.__init__(self, event)
        self.server_version = self.data['server_version']


class PostedEvent(Event):
    event = 'posted'

    def __init__(self, data):
        Event.__init__(self, data)
        self.mentions = []
        if 'mentions' in self.data:
            self.mentions = json.loads(self.data['mentions'])

        for k, v in json.loads(self.data['post']).items():
            self.__setattr__(k, v)

    def is_mentioned(self, bot):
        if bot.userid in self.mentions:
            return True
        return False


AVAILABLE = {
    'hello': HelloEvent,
    'posted': PostedEvent
}
