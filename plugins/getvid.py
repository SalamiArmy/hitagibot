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

    vidurl = 'https://www.googleapis.com/youtube/v3/search'
    args = {'key': keyConfig['Google']['GCSE_APP_ID'],
            'part': 'snippet',
            'safeSearch': 'none',
            'q': requestText,
            'type': 'video'}
    realUrl = vidurl + '?' + urllib.parse.urlencode(args)
    data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
    if 'items' in data and len(data['items']) >= 1:
        vidlink = data['items'][0]['id']['videoId']
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        return bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') +
                                                     'https://www.youtube.com/watch?v=' + vidlink + '&type=video')

    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    return bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                 ', I\'m afraid I can\'t do that.\n(Video not found)')

plugin_info = {
    'name': "Get Vid",
    'desc': "Gets videos from Google's Youtube API."
}

arguments = {
    'text': [
        "(?i)^[\/](getvid) (.*)"
    ]
}
