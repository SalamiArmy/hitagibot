# coding=utf-8
import configparser

import telegram

from mcstatus import MinecraftServer


def main(tg):
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = configparser.ConfigParser()
    keyConfig.read(["keys.ini", "config.ini", "..\keys.ini", "..\config.ini"])

    bot = telegram.Bot(keyConfig['BOT_CONFIG']['token'])

    mcServer = keyConfig.get('Minecraft', 'SVR_ADDR')
    mcPort = int(keyConfig.get('Minecraft', 'SVR_PORT'))
    dynmapPort = keyConfig.get('Minecraft', 'DYNMAP_PORT')
    error = False
    try:
        status = MinecraftServer(mcServer, mcPort).status()
    except IOError:
        error = True
    if not error:
        bot.sendChatAction(chat_id=tg.message['chat']['id'], action=telegram.ChatAction.TYPING)
        return bot.sendMessage(chat_id=tg.message['chat']['id'], text=('The server at {0} has {1} players and replied in {2} ms' +
                                                                       ('' if dynmapPort == '' else '\nSee map: ' + mcServer + ':' + dynmapPort)) \
                               .format(mcServer + ':' + str(mcPort), status.players.online, status.latency))

    user = tg.message['from']['username'] \
        if not tg.message['from']['username'] == '' \
        else tg.message['from']['first_name'] + (' ' + tg.message['from']['last_name']) \
        if not tg.message['from']['last_name'] == '' \
        else 'Dave'
    bot.sendChatAction(chat_id=tg.message['chat']['id'], action=telegram.ChatAction.TYPING)
    return bot.sendMessage(chat_id=tg.message['chat']['id'], text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                                                  ', I\'m afraid I cannot find the Minecraft server at ' + \
                                                                  mcServer + ':' + str(mcPort))

plugin_info = {
    'name': "Minecraft",
    'desc': "Gets info from Minecraft Server."
}

arguments = {
    'text': [
        "(?i)^[\/](mc)"
    ]
}
