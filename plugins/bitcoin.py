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

    try:
        bcurl = 'https://api.coindesk.com/v1/bpi/currentprice/ZAR.json'
        data = json.loads(urllib.request.urlopen(bcurl).read().decode('utf-8'))
        bcurl2 = 'https://api.coindesk.com/v1/bpi/currentprice.json'
        data2 = json.loads(urllib.request.urlopen(bcurl2).read().decode('utf-8'))
        updateTime = data['time']['updated']
        priceUS = data['bpi']['USD']
        priceZA = data['bpi']['ZAR']
        priceGB = data2['bpi']['GBP']
        bot.sendChatAction(chat_id=tg.message['chat']['id'], action=telegram.ChatAction.TYPING)
        return bot.sendMessage(chat_id=tg.message['chat']['id'],
                               text='The Current Price of 1 Bitcoin:\n\n' + priceUS['rate'] +
                                    ' USD\n' + priceGB['rate'] +
                                    ' GBP\n' + priceZA['rate'] + ' ZAR' + '\n\nTime Updated: ' + updateTime)
    except Exception:
        user = tg.message['from']['username'] \
            if not tg.message['from']['username'] == '' \
            else tg.message['from']['first_name'] + (' ' + tg.message['from']['last_name']) \
                if not tg.message['from']['last_name'] == '' \
                else 'Dave'
        return tg.send_message('I\'m sorry ' + user + ', I\'m afraid I can\'t find any Bitcoin exchange rates.')

plugin_info = {
    'name': "BitCoin",
    'desc': "Gets BitCoin exchange rate from CoinDesk's API."
}

arguments = {
    'text': [
        "(?i)^[\/](bitcoin)"
    ]
}
