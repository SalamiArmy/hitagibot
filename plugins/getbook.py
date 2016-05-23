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

    booksUrl = 'https://www.googleapis.com/books/v1/volumes?maxResults=1&key=' + \
               keyConfig.get('Google', 'GCSE_APP_ID') + '&q='
    realUrl = booksUrl + requestText
    data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
    if 'totalItems' in data and data['totalItems'] >= 1:
        bookData = data['items'][0]['volumeInfo']
        googleBooksUrl = data['items'][0]['accessInfo']['webReaderLink']
        if 'imageLinks' in bookData:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            userWithCurrentChatAction = chat_id
            urlForCurrentChatAction = 'Photo= ' + bookData['imageLinks']['thumbnail'] + \
                                      ' Caption= ' + (user + ': ' if not user == '' else '') + googleBooksUrl
            bot.sendPhoto(chat_id=userWithCurrentChatAction, photo=bookData['imageLinks']['thumbnail'],
                          caption=(user + ': ' if not user == '' else '') + googleBooksUrl)
        else:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            userWithCurrentChatAction = chat_id
            urlForCurrentChatAction = (user + ': ' if not user == '' else '') + googleBooksUrl
            bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I can\'t find any books for ' + \
                                  requestText + '.'
        bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)

plugin_info = {
    'name': "Book",
    'desc': "Gets book information from Google Book's API."
}

arguments = {
    'text': [
        "^[/](getbook) (.*)"
    ]
}
