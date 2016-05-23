# coding=utf-8
import logging
import urllib

import telegram
# reverse image search imports:
import json


def main(tg):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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

    movieUrl = 'http://www.omdbapi.com/?plot=short&r=json&y=&t='
    realUrl = movieUrl + requestText
    data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
    if 'Error' not in data:
        if 'Poster' in data and not data['Poster'] == 'N/A':
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            userWithCurrentChatAction = chat_id
            urlForCurrentChatAction = data['Poster']
            bot.sendPhoto(chat_id=userWithCurrentChatAction, photo=urlForCurrentChatAction,
                          caption=(user if not user == '' else '') + data['Title'] + ':\n' + data['Plot'])
        else:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            userWithCurrentChatAction = chat_id
            urlForCurrentChatAction = (user + ': ' if not user == '' else '') + \
                                      data['Title'] + ':\n' + data['Plot']
            bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I can\'t find any movies for ' + \
                                  requestText + '.'
        bot.sendMessage(chat_id=userWithCurrentChatAction,
                        text=urlForCurrentChatAction)

plugin_info = {
    'name': "Movie",
    'desc': "Gets movie info from Open Movie Database API."
}

arguments = {
    'text': [
        "^[/](getmovie) (.*)"
    ]
}
