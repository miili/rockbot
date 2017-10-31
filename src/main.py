#!/usr/bin/env python3
import logging
import json
import os

from pyrocko import guts
from mattermostdriver import Driver as MattermostDriver

from rockbot import events
from rockbot import handlers

op = os.path

class BotConfig(guts.Object):
    url = guts.String.T(
        help='Mattermost Server URL',
        default='hive.pyrocko.org')
    port = guts.Int.T(
        help='Portnumber',
        default=80,)
    username = guts.String.T(
        help='Username',
        default='None')
    password = guts.String.T(
        help='Password',
        default='None')
    token = guts.String.T(
        help='Login token, replacing username/password',
        default='None')
    channel = guts.String.T(
        help='Bots main channel',
        default='bot_test')
    team = guts.String.T(
        help='Team name',
        default='pyrocko-dev')

    def get_bot(c):
        if c.token == 'None':
            c.token = None
        else:
            c.username = None
            c.password = None   

        return RockBot(
            url=c.url,
            port=c.port,
            login_id=c.username,
            password=c.password,
            token=c.token,
            channel=c.channel,
            team=c.team)


class RockBot(MattermostDriver):

    def __init__(self, url, login_id=None, password=None,
                 token=None, port=80, channel=None, team=None):

        self.driver_args = {
            'url': url,
            'login_id': login_id,
            'password': password,
            'token': token,
            'scheme': 'https',
            'port': port,
            'basepath': '/api/v4',
            'timeout': 30,
            }

        MattermostDriver.__init__(self, self.driver_args)
        self.log = logging.getLogger('rockbot')

        self.channel = channel
        self.team = team

        self.handlers = []
        self.init_handlers()

    def connect(self):
        self.log.info('Logging into %s:%d ...'
            % (self.driver_args['url'], self.driver_args['port']))
        self.login()
        self.channel_id = self.get_channel_id(
            self.team, self.channel)['id']
        self.userid = self.client.userid

        self.post('%s is alive! :heart:' % self.__class__.__name__)
        self.loop = self.init_websocket(self.event_handler)

    def init_handlers(self):
        for h in handlers.AVAILABLE:
            handler = h(self)
            self.handlers.append(handler)
            self.log.info('Added handler %s' % handler.__class__.__name__)

    def get_channel_id(self, team_name, channel_name):
        r = self.api['channels'].get_channel_by_name_and_team_name(
                team_name=team_name,
                channel_name=channel_name)
        return r

    def post(self, message):
        self.log.info('Posting into %s: %s' % (self.channel, message))
        self.api['posts']\
            .create_post({
                'channel_id': self.channel_id,
                'message': message
            })

    async def event_handler(self, *args):
        data = json.loads(args[0])
        # print(json.dumps(data, sort_keys=True,
        #                  indent=4, separators=(',', ': ')))
        if 'event' in data:
            if data['event'] in events.AVAILABLE:
                ev = events.AVAILABLE[data['event']](data)
                await self.process_event(ev)
                return
        self.log.debug('Could not handle *%s*' % data)

    async def process_event(self, event):
        for handler in self.handlers:
            if event.__class__ in handler.hooks:
                handler.process(event)



def create_config(filename):
    config = BotConfig(
        url='mattermost.server.org')
    if op.exists(filename):
        print('File already %s exists, not overwriting!' % filename)
        return
    config.dump(filename=filename)
    print('Sample config dumped to %s' % filename)

def run(filename):
    config = guts.load(filename=filename)
    bot = config.get_bot()
    bot.connect()
    return bot

def main():
    import argparse
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''\
available actions
  run     Start the rockbot
  init    Init a new rockbot config file
''')
    parser.add_argument(
        'action',
        help='action to perform',
        choices=['run', 'init']
        )
    parser.add_argument(
        'filename',
        help='config file name',
        )
    parser.add_argument(
        '-d', '--debug',
        help='Show debug output',
        action='store_true')
    args = parser.parse_args()

    filename = op.abspath(args.filename)

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if args.action == 'run':
        run(filename)

    if args.action == 'init':
        create_config(filename)

if __name__ == '__main__':
    main()
