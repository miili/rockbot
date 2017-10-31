import re
from datetime import datetime
from rockbot.events import HelloEvent, PostedEvent


class RockHandler(object):
    hooks = []

    def __init__(self, bot):
        self.bot = bot
        self.log = bot.log.getChild(self.__class__.__name__)

    def process(self, event):
        raise NotImplementedError()

    @staticmethod
    def mentioned(func):
        def wrapper(self, event):
            if isinstance(event, PostedEvent):
                if event.is_mentioned(self.bot.userid):
                    func(self, event)
        return wrapper


class VersionHandler(RockHandler):
    hooks = [HelloEvent]

    def process(self, event):
        self.log.info('Connected to server version %s' % event.server_version)


class PingHandler(RockHandler):
    hooks = [PostedEvent]
    match = re.compile(r'[pP]ing')

    @RockHandler.mentioned
    def process(self, event):
        if len(self.match.findall(event.message)) > 0:
            self.bot.post('Pong!')


class AgeHandler(RockHandler):
    hooks = [PostedEvent]
    match = re.compile(r'how old are you|uptime')

    def __init__(self, *args, **kwargs):
        RockHandler.__init__(self, *args, **kwargs)
        self.starttime = datetime.now()

    @RockHandler.mentioned
    def process(self, event):
        if len(self.match.findall(event.message)) > 0:
            self.bot.post('I am %s old!'
                          % (datetime.now() - self.starttime))
