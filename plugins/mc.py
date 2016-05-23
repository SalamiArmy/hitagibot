# coding=utf-8
import configparser
import logging

import telegram
# reverse image search imports:

from mcstatus import MinecraftServer


def main(tg):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = configparser.ConfigParser()
    keyConfig.read(["keys.ini", "config.ini", "..\keys.ini", "..\config.ini"])

    chat_id = tg.message['chat']['id']
    message = tg.message['text']
    botName = tg.misc['bot_info']['username']

    message = message.replace(botName, "")

    splitText = message.split(' ', 1)

    requestText = splitText[1] if ' ' in message else ''

    bot = telegram.Bot(keyConfig['BOT_CONFIG']['token'])

    mcServer = keyConfig.get('Minecraft', 'SVR_ADDR')
    mcPort = int(keyConfig.get('Minecraft', 'SVR_PORT'))
    dynmapPort = keyConfig.get('Minecraft', 'DYNMAP_PORT')
    status = MinecraftServer(mcServer, mcPort).status()
    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    userWithCurrentChatAction = chat_id
    urlForCurrentChatAction = ('The server at {0} has {1} players and replied in {2} ms' +
                               ('' if dynmapPort == '' else '\nSee map: ' + mcServer + ':' + dynmapPort))\
        .format(mcServer + ':' + str(mcPort), status.players.online, status.latency)
    bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)

plugin_info = {
    'name': "Minecraft",
    'desc': "Gets info from Minecraft Server."
}

arguments = {
    'text': [
        "^[/](mc)"
    ]
}
