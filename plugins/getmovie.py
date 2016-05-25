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

    movieUrl = 'http://www.omdbapi.com/'
    args = {'t': requestText,
            'plot': 'short',
            'searchType': 'image',
            'r': 'json'}
    realUrl = movieUrl + '?' + urllib.parse.urlencode(args)
    data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
    if 'Error' not in data:
        if 'Poster' in data and not data['Poster'] == 'N/A':
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            return bot.sendPhoto(chat_id=chat_id, photo=data['Poster'],
                                 caption=(user if not user == '' else '') + '*' + data['Title'] + '*\n' + data['Plot'],
                                 parse_mode='Markdown')
        else:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            return bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + \
                                                         '*' + data['Title'] + '*\n' + data['Plot'],
                                   parse_mode='Markdown')

    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    return bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                              ', I\'m afraid I can\'t find any movies for ' + \
                              requestText + '.')

plugin_info = {
    'name': "Movie",
    'desc': "Gets movie info from Open Movie Database API."
}

arguments = {
    'text': [
        "(?i)^[\/](getmovie) (.*)"
    ]
}
