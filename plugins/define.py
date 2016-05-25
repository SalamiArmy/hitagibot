import configparser

#coding= utf - 8
import random

import telegram
import urllib
import xmltodict

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
        else 'Dave'
    botName = tg.misc['bot_info']['username']

    message = message.replace(botName, "")

    splitText = message.split(' ', 1)

    requestText = splitText[1] if ' ' in message else ''

    bot = telegram.Bot(keyConfig['BOT_CONFIG']['token'])
    
    dicUrl = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/'
    realUrl = dicUrl + requestText + '?key=' + keyConfig.get('Merriam-Webster', 'API_KEY')
    data = xmltodict.parse(urllib.request.urlopen(realUrl).read().decode('utf-8'))
    if len(data['entry_list']) >= 1:
        partOfSpeech = data['entry_list']['entry']['fl']
        if len(partOfSpeech) >= 1:
            getAllDefs = data['entry_list']['entry']['def']['dt']
            if type(getAllDefs) is list:
                definitionText = getAllDefs[random.randint(0, len(getAllDefs) - 1)]['#text'].replace(':', '')
            else:
                definitionText = getAllDefs['#text'].replace(':', '')
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            return bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + \
                                                         requestText.title() + ":\n" + \
                                                         partOfSpeech + ".\n\n" + definitionText)

    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    return bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + user + \
                                                 ', I\'m afraid I can\'t find any definitions for the word ' + \
                                                 requestText + '.')

############################# Ashley: http://dictionaryapi.net/ is down! ###############################
# dicUrl = 'http://dictionaryapi.net/api/definition/'
# realUrl = dicUrl + requestText
# data = json.load(urllib.urlopen(realUrl))
# if len(data) >= 1:
#     partOfSpeech = data[random.randint(0, len(data) - 1)]
#     if len(partOfSpeech['Definitions']) >= 1:
#         definitionText = partOfSpeech['Definitions'][0]
#         bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
#         userWithCurrentChatAction = chat_id
#         urlForCurrentChatAction = (user + ': ' if not user == '' else '') +\
#                                   requestText.title() + ":\n" + \
#                                   partOfSpeech['PartOfSpeech'] + ".\n\n" + definitionText
#         bot.sendMessage(chat_id=chat_id, text=urlForCurrentChatAction)
#     else:
#         bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
#         userWithCurrentChatAction = chat_id
#         urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
#                                   ', I\'m afraid I can\'t find any definitions for the word ' +\
#                                   requestText + '.'
#         bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)
# else:
#     bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
#     userWithCurrentChatAction = chat_id
#     urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
#                               ', I\'m afraid I can\'t find any definitions for the word ' +\
#                               requestText + '.'
#     bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)

plugin_info = {
    'name': "Define",
    'desc': "Gets english dictionary definitions from Merriam-Webster Dictionary API."
}

arguments = {
    'text': [
        "(?i)^[\/](define) (.*)"
    ]
}
