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

    bot = telegram.Bot(keyConfig['BOT_CONFIG']['token'])

    allMatchesUrl = 'http://cricscore-api.appspot.com/csa'
    allMatches = json.loads(urllib.request.urlopen(allMatchesUrl).read().decode('utf-8'))
    proteasMatchId = None
    for match in allMatches:
        if match['t1'] == 'South Africa' or match['t2'] == 'South Africa':
            proteasMatchId = match['id']
    if proteasMatchId != None:
        matchesUrl = 'http://cricscore-api.appspot.com/csa?id=' + str(proteasMatchId)
        match = json.loads(urllib.request.urlopen(matchesUrl).read().decode('utf-8'))
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        return bot.sendMessage(chat_id=chat_id, text=(match[0]['si'] + '\n' + match[0]['de']))

    user = tg.message['from']['username'] \
        if not tg.message['from']['username'] == '' \
        else tg.message['from']['first_name'] + (' ' + tg.message['from']['last_name']) \
        if not tg.message['from']['last_name'] == '' \
        else 'Dave'
    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    return bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + user + ', I\'m afraid the Proteas are not playing right now.')

plugin_info = {
    'name': "Cricket",
    'desc': "Gets info about the current Proteas cricket game from CricScore's API."
}

arguments = {
    'text': [
        "(?i)^[\/](cric)"
    ]
}
