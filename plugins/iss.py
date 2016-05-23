# coding=utf-8
import configparser
import datetime
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

    
    mapsUrl = 'https://maps.googleapis.com/maps/api/place/textsearch/json?key=' + \
              keyConfig.get('Google', 'GCSE_APP_ID') + '&location=-30,30&radius=50000&query='
    realUrl = mapsUrl + requestText
    data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
    if len(data['results']) >= 1:
        latNum = data['results'][0]['geometry']['location']['lat']
        lngNum = data['results'][0]['geometry']['location']['lng']
        issSightingsUrl = 'http://api.open-notify.org/iss-pass.json?lat='
        realUrl = issSightingsUrl + str(latNum) + '&lon=' + str(lngNum)
        data = json.load(urllib.urlopen(realUrl))
        if len(data['response']) >= 1:
            timeStamp = data['response'][0]['risetime']
            durationSeconds = data['response'][0]['duration']
            startDateTime = datetime.datetime.fromtimestamp(timeStamp)
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + \
                                      'The next ISS sighting in ' + requestText.title() + \
                                      ' starts at ' + startDateTime.strftime('%H:%M:%S on %d-%m-%Y') + \
                                      ' for ' + str(divmod(durationSeconds, 60)[0]) + \
                                      ' minutes and ' + str(divmod(durationSeconds, 60)[1]) + ' seconds.')
        else:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            userWithCurrentChatAction = chat_id
            urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                      ', I\'m afraid I can\'t find the next ISS sighting for ' + \
                                      requestText + '.'
            bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        bot.sendMessage(chat_id=chat_id, text=requestText)

plugin_info = {
    'name': "ISS",
    'desc': "Gets the next sighting of the International Space Station for a given place."
}

arguments = {
    'text': [
        "^[/](iss) (.*)"
    ]
}
