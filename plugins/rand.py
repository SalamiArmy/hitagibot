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

    usdurl = 'http://api.fixer.io/latest?base=USD'
    gbpurl = 'http://api.fixer.io/latest?base=GBP'
    eururl = 'http://api.fixer.io/latest?base=EUR'
    data1 = json.loads(urllib.request.urlopen(usdurl).read().decode('utf-8'))
    data2 = json.loads(urllib.request.urlopen(gbpurl).read().decode('utf-8'))
    data3 = json.loads(urllib.request.urlopen(eururl).read().decode('utf-8'))
    zarusd = float(data1['rates']['ZAR'])
    zargbp = float(data2['rates']['ZAR'])
    zareur = float(data3['rates']['ZAR'])
    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    userWithCurrentChatAction = chat_id
    urlForCurrentChatAction = '1 USD = ' + str(zarusd) + ' ZAR\n1 GBP = ' + str(zargbp) + \
                              ' ZAR\n1 EUR = ' + str(zareur) + ' ZAR'
    bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)

plugin_info = {
    'name': "Rand",
    'desc': "Gets exchange rate info for the Rand."
}

arguments = {
    'text': [
        "^[/](rand)"
    ]
}
