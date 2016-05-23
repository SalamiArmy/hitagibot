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

    translateUrl = 'https://www.googleapis.com/language/translate/v2?key=' + \
                   keyConfig.get('Google', 'GCSE_APP_ID') + '&target=en&q='
    realUrl = translateUrl + requestText
    data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
    if len(data['data']['translations']) >= 1:
        translation = data['data']['translations'][0]['translatedText']
        detectedLanguage = data['data']['translations'][0]['detectedSourceLanguage']
        languagesList = json.load(urllib.urlopen(
            'https://www.googleapis.com/language/translate/v2/languages?target=en&key=' + keyConfig.get(
                'Google', 'GCSE_APP_ID')))['data']['languages']
        detectedLanguageSemanticName = [lang for lang in languagesList
                                        if lang['language'] == detectedLanguage][0]['name']
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + \
                                  "Detected language: " + detectedLanguageSemanticName + \
                                  "\nMeaning: " + translation.title())
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I can\'t find any translations for ' + \
                                  requestText + '.')

plugin_info = {
    'name': "Translate",
    'desc': "Gets translations to english from Google's Translation API."
}

arguments = {
    'text': [
        "^[/](translate) (.*)"
    ]
}
