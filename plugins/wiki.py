# coding=utf-8
import configparser
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

    wikiUrl = \
        'https://simple.wikipedia.org/w/api.php?action=opensearch&limit=1&namespace=0&format=json&search='
    realUrl = wikiUrl + requestText
    data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
    if len(data[2]) >= 1:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + \
                                  data[2][0] + '\nLink: ' + data[3][0], disable_web_page_preview=True)
    else:
        wikiUrl = \
            'https://en.wikipedia.org/w/api.php?action=opensearch&limit=1&namespace=0&format=json&search='
        realUrl = wikiUrl + requestText
        data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
        if len(data[2]) >= 1 and not data[2][0] == '':
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            userWithCurrentChatAction = chat_id
            urlForCurrentChatAction = (user + ': ' if not user == '' else '') + \
                                      data[2][0] + '\nLink: ' + data[3][0]
            bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction,
                            disable_web_page_preview=True)
        else:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            bot.sendMessage(chat_id=chat_id,
                            text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                      ', I\'m afraid I can\'t find any wiki articles for ' + \
                                      requestText + '.')

plugin_info = {
    'name': "Wiki",
    'desc': "Gets Wikipedia info from Wikipedia's API."
}

arguments = {
    'text': [
        "^[/](wiki) (.*)"
    ]
}
