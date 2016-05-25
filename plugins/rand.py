# coding=utf-8
import configparser
import urllib

import telegram
import json


def main(tg):
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = configparser.ConfigParser()
    keyConfig.read(["keys.ini", "config.ini", "..\keys.ini", "..\config.ini"])

    bot = telegram.Bot(keyConfig['BOT_CONFIG']['token'])

    usdurl = 'http://api.fixer.io/latest?base=USD'
    gbpurl = 'http://api.fixer.io/latest?base=GBP'
    eururl = 'http://api.fixer.io/latest?base=EUR'
    data1 = json.loads(urllib.request.urlopen(usdurl).read().decode('utf-8'))
    data2 = json.loads(urllib.request.urlopen(gbpurl).read().decode('utf-8'))
    data3 = json.loads(urllib.request.urlopen(eururl).read().decode('utf-8'))
    if 'rates' in data1 and 'rates' in data2 and 'rates' in data3:
        zarusd = float(data1['rates']['ZAR'])
        zargbp = float(data2['rates']['ZAR'])
        zareur = float(data3['rates']['ZAR'])
        bot.sendChatAction(chat_id=tg.message['chat']['id'], action=telegram.ChatAction.TYPING)
        return bot.sendMessage(chat_id=tg.message['chat']['id'], text='1 USD = ' + str(zarusd) +
                                                                      ' ZAR\n1 GBP = ' + str(zargbp) +
                                                                      ' ZAR\n1 EUR = ' + str(zareur) + ' ZAR')


    user = tg.message['from']['username'] \
        if not tg.message['from']['username'] == '' \
        else tg.message['from']['first_name'] + (' ' + tg.message['from']['last_name']) \
        if not tg.message['from']['last_name'] == '' \
        else ''
    bot.sendChatAction(chat_id=tg.message['chat']['id'], action=telegram.ChatAction.TYPING)
    return bot.sendMessage(chat_id=tg.message['chat']['id'], text='I\'m sorry ' + (user if not user == '' else 'Dave') +\
                                                         ', I\'m afraid I can\'t find any currency exchange rate information')

plugin_info = {
    'name': "Rand",
    'desc': "Gets exchange rate info for the Rand."
}

arguments = {
    'text': [
        "(?i)^[\/](rand)"
    ]
}
