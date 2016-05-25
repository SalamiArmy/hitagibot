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

    mapsUrl = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    args = {'key': keyConfig['Google']['GCSE_APP_ID'],
            'location': '-30,30',
            'radius': 50000,
            'query': requestText}
    realUrl = mapsUrl + '?' + urllib.parse.urlencode(args)
    data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
    if len(data['results']) >= 1:
        latNum = data['results'][0]['geometry']['location']['lat']
        lngNum = data['results'][0]['geometry']['location']['lng']
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.FIND_LOCATION)
        return bot.sendLocation(chat_id=chat_id, latitude=latNum, longitude=lngNum)

    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    return bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                                 ', I\'m afraid I can\'t find any places for ' + \
                                                 requestText + '.')

plugin_info = {
    'name': "Places",
    'desc': "Gets place locations from Google Maps' Places API."
}

arguments = {
    'text': [
        "(?i)^[\/](place) (.*)"
    ]
}
