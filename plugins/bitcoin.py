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

    bot = telegram.Bot(keyConfig['BOT_CONFIG']['token'])

    bcurl = 'https://api.coindesk.com/v1/bpi/currentprice/ZAR.json'
    data = json.loads(urllib.request.urlopen(bcurl).read().decode('utf-8'))
    bcurl2 = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    data2 = json.loads(urllib.request.urlopen(bcurl2).read().decode('utf-8'))
    updateTime = data['time']['updated']
    priceUS = data['bpi']['USD']
    priceZA = data['bpi']['ZAR']
    priceGB = data2['bpi']['GBP']
    bot.sendChatAction(chat_id=tg.message['chat']['id'], action=telegram.ChatAction.TYPING)
    bot.sendMessage(chat_id=tg.message['chat']['id'],
                    text='The Current Price of 1 Bitcoin:\n\n' + priceUS['rate'] +
                         ' USD\n' + priceGB['rate'] +
                         ' GBP\n' + priceZA['rate'] + ' ZAR' + '\n\nTime Updated: ' + updateTime)

plugin_info = {
    'name': "BitCoin",
    'desc': "Gets BitCoin exchange rate from CoinDesk's API."
}

arguments = {
    'text': [
        "^[/](bitcoin)"
    ]
}
