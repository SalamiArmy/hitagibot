# coding=utf-8
import configparser
import urllib

import telegram
import json


def main(tg):
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = configparser.ConfigParser()
    keyConfig.read(["keys.ini", "config.ini", "..\keys.ini", "..\config.ini"])

    chat_id = tg.message['chat']['id']
    message = tg.message['text']
    user = tg.message['from']['username'] \
        if not tg.message['from']['username'] == '' \
        else tg.message['from']['first_name'] + (' ' + tg.message['from']['last_name']) \
        if not tg.message['from']['last_name'] == '' \
        else ''
    botName = tg.misc['bot_info']['username']

    message = message.replace(botName, "")

    splitText = message.split(' ', 1)

    requestText = splitText[1] if ' ' in message else ''

    bot = telegram.Bot(keyConfig['BOT_CONFIG']['token'])

    tor1Url = 'https://torrentproject.se/?s='
    searchUrl = tor1Url + requestText + '&out=json'
    data = json.loads(urllib.request.urlopen(searchUrl).read().decode('utf-8'))
    torrageUrl = 'http://torrage.info/torrent.php?h='
    if int(data['total_found']) >= 1 and '1' in data:
        torrent = data['1']['torrent_hash']
        tTitle = data['1']['title']
        seeds = str(data['1']['seeds'])
        leechs = str(data['1']['leechs'])
        downloadUrl = torrageUrl + torrent.upper()
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        return bot.sendMessage(chat_id=chat_id, text='Torrent Name: ' + tTitle + \
                                                     '\nDownload Link: ' + downloadUrl + \
                                                     '\nSeeds: ' + seeds + \
                                                     '\nLeechers: ' + leechs, disable_web_page_preview=True)

    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    return bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                                 ', I can\'t find any torrents for ' + \
                                                 requestText + '.')

plugin_info = {
    'name': "Torrent",
    'desc': "Gets torrent info from TorRage's API."
}

arguments = {
    'text': [
        "(?i)^[\/](torrent) (.*)"
    ]
}
