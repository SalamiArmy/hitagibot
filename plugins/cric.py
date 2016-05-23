# coding=utf-8
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

    allMatchesUrl = 'http://cricscore-api.appspot.com/csa'
    allMatches = json.load(urllib.request.urlopen(allMatchesUrl))
    proteasMatchId = None
    for match in allMatches:
        if match['t1'] == 'South Africa' or match['t2'] == 'South Africa':
            proteasMatchId = match['id']
    if proteasMatchId == None:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid the Proteas are not playing right now.'
        bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)
    else:
        matchesUrl = 'http://cricscore-api.appspot.com/csa?id=' + str(proteasMatchId)
        match = json.load(urllib.urlopen(matchesUrl))
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = (match[0]['si'] + '\n' + match[0]['de'])
        bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)

plugin_info = {
    'name': "Cricket",
    'desc': "Gets info about the current Proteas cricket game from CricScore's API."
}

arguments = {
    'text': [
        "^[/](cric)"
    ]
}
