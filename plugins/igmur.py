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
    botName = tg.misc['bot_info']['username']

    message = message.replace(botName, "")

    splitText = message.split(' ', 1)

    requestText = splitText[1] if ' ' in message else ''

    bot = telegram.Bot(keyConfig['BOT_CONFIG']['token'])

    client_id = keyConfig.get('Imgur', 'CLIENT_ID')
    client_secret = keyConfig.get('Imgur', 'CLIENT_SECRET')
    client = ImgurClient(client_id, client_secret)
    items = client.gallery_search(q=string.capwords(requestText),
                                  sort='top',
                                  window='all')
    if len(items) > 0:
        if items[0].link.endswith('.gif'):
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            return bot.sendDocument(chat_id=chat_id,
                                    filename=requestText,
                                    document=items[0].link)
        else:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            return bot.sendPhoto(chat_id=chat_id,
                                 filename=requestText,
                                 photo=items[0].link)


plugin_info = {
    'name': "Imgur",
    'desc': "Gets Imgur images!"
}

arguments = {
    'text': [
        "^[/](imgur) (.*)"
    ]
}
