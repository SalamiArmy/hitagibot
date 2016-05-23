import configparser
import logging
import random
import string
import telegram
from imgurpython import ImgurClient


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

    client_id = keyConfig.get('Imgur', 'CLIENT_ID')
    client_secret = keyConfig.get('Imgur', 'CLIENT_SECRET')
    client = ImgurClient(client_id, client_secret)
    items = client.gallery_search(q=string.capwords(requestText),
                                  advanced={'q_type': 'anigif'},
                                  sort='top',
                                  window='all',
                                  page=random.randint(0, 9))
    for item in items:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = item.link
        bot.sendDocument(chat_id=userWithCurrentChatAction,
                         filename=requestText,
                         document=urlForCurrentChatAction)


plugin_info = {
    'name': "Get",
    'desc': "Gets Imgur images!"
}

arguments = {
    'text': [
        "^[/](imgur) (.*)"
    ]
}
