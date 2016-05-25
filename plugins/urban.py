# coding=utf-8
import configparser
import random
import string
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

    dicurl = 'http://api.urbandictionary.com/v0/define'
    realUrl = dicurl + '?' + urllib.parse.urlencode({'term': requestText})
    data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
    if 'list' in data and len(data['list']) >= 1:
        resultNum = data['list'][random.randint(0, len(data['list']) - 1)]
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        return bot.sendMessage(chat_id=chat_id,
                               text=(user + ': ' if not user == '' else '') + \
                                    'Urban Definition For ' + string.capwords(requestText) + ":\n" + \
                                    resultNum['definition'] + \
                                    '\n\nExample:\n' + resultNum['example'])

    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    return bot.sendMessage(chat_id=chat_id,
                           text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                ', I\'m afraid I can\'t find any urban definitions for ' + \
                                string.capwords(requestText) + '.')

plugin_info = {
    'name': "Urban Dictionary",
    'desc': "Gets Urban Dictionary definitions from Urban Dictionary API."
}

arguments = {
    'text': [
        "(?i)^[\/](urban) (.*)"
    ]
}
