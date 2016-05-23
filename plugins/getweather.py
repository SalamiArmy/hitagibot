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

    yahoourl = \
        "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20" \
        "in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%27" + requestText + "%27)%20" \
                       "and%20u%3D%27c%27&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
    result = urllib.urlopen(yahoourl).read().decode('utf-8')
    data = json.loads(result)
    if data['query']['count'] == 1:
        weather = data['query']['results']['channel']['item']['condition']
        forecast = data['query']['results']['channel']['item']['forecast']
        city = data['query']['results']['channel']['location']['city']
        astronomy = data['query']['results']['channel']['astronomy']
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        bot.sendMessage(chat_id=chat_id,
                        text=('It is currently ' + weather['text'] + ' in ' + city +
                                   ' with a temperature of ' + weather['temp'] + 'C.\nA high of ' +
                                   forecast[0]['high'] + ' and a low of ' + forecast[0]['low'] +
                                   ' are expected during the day with conditions being ' +
                                   forecast[0]['text'] + '.\nSunrise: ' + astronomy['sunrise'] +
                                   '\nSunset: ' + astronomy['sunset']),
                        parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I don\'t know the place ' + \
                                  requestText + '.')

plugin_info = {
    'name': "Get Weather",
    'desc': "Gets weather info from Yahoo's API."
}

arguments = {
    'text': [
        "^[/](getgetweather) (.*)"
    ]
}
