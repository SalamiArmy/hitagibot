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

    yahoourl = 'https://query.yahooapis.com/v1/public/yql'
    args = {'q': 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\'' + requestText + '\') and u=\'c\'',
            'format': 'json',
            'env': 'store://datatables.org/alltableswithkeys'}
    realUrl = yahoourl + '?' + urllib.parse.urlencode(args)
    data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
    if data['query']['count'] == 1:
        weather = data['query']['results']['channel']['item']['condition']
        forecast = data['query']['results']['channel']['item']['forecast']
        city = data['query']['results']['channel']['location']['city']
        astronomy = data['query']['results']['channel']['astronomy']
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        return bot.sendMessage(chat_id=chat_id,
                               text=('It is currently ' + weather['text'] + ' in ' + city +
                                     ' with a temperature of ' + weather['temp'] + 'C.\nA high of ' +
                                     forecast[0]['high'] + ' and a low of ' + forecast[0]['low'] +
                                     ' are expected during the day with conditions being ' +
                                     forecast[0]['text'] + '.\nSunrise: ' + astronomy['sunrise'] +
                                     '\nSunset: ' + astronomy['sunset']),
                               parse_mode=telegram.ParseMode.MARKDOWN)

    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    return bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                                 ', I\'m afraid I don\'t know the place ' + \
                                                 requestText + '.')

plugin_info = {
    'name': "Get Weather",
    'desc': "Gets weather info from Yahoo's API."
}

arguments = {
    'text': [
        "(?i)^[\/](getweather) (.*)"
    ]
}
