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

    googurl = 'https://www.googleapis.com/customsearch/v1?&searchType=image&num=10&safe=off&' \
              'cx=' + keyConfig.get('Google', 'GCSE_SE_ID') + '&key=' + keyConfig.get('Google',
                                                                                      'GCSE_APP_ID') + '&q='
    realUrl = googurl + requestText.encode('utf-8') + "&fileType=gif"
    data = json.load(urllib.urlopen(realUrl))
    if 'items' in data and len(data['items']) >= 1:
        imagelink = data['items'][random.randint(0, 9)]['link']
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        bot.sendDocument(chat_id=chat_id,
                         filename=requestText,
                         document=imagelink)
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +\
                                  ', I\'m afraid I can\'t find a gif for ' +\
                                  string.capwords(requestText) + '.')


plugin_info = {
    'name': "Get Gif",
    'desc': "Gets gifs from Google's Custom Search API."
}

arguments = {
    'text': [
        "^[/](getgif) (.*)"
    ]
}
