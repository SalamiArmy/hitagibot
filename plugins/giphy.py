import configparser
import json
import logging
import random
import string
import urllib

import telegram


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

    giphyUrl = 'http://api.giphy.com/v1/gifs/search?q='
    apiKey = '&api_key=dc6zaTOxFJmzC&limit=10&offset=0'
    realUrl = giphyUrl + requestText.encode('utf-8') + apiKey
    data = json.load(urllib.urlopen(realUrl))
    if data['pagination']['total_count'] >= 1:
        imagelink = data['data'][random.randint(0, len(data['data']) - 1)]['images']['original']['url']
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_DOCUMENT)
        bot.sendDocument(chat_id=chat_id,
                         filename=imagelink + '.gif',
                         document=imagelink.encode('utf-8'))
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        bot.sendMessage(chat_id=chat_id,
                        text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I can\'t find a giphy gif for ' + \
                                  string.capwords(requestText.encode('utf-8')) + '.')


plugin_info = {
    'name': "Giphy",
    'desc': "Gets Giphy gifs."
}

arguments = {
    'text': [
        "^[/](getgif) (.*)"
    ]
}
