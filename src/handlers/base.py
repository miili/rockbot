from rockbot.events import HelloEvent


class RockHandler(object):
    hooks = []

    def __init__(self, bot):
        self.bot = bot
        self.log = bot.log.getChild(self.__class__.__name__)

    def process(self, event):
        raise NotImplementedError()


class VersionHandler(RockHandler):
    hooks = [HelloEvent]

    def process(self, event):
        self.log.info('Connected to server version %s' % event.server_version)
