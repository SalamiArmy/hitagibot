# coding=utf-8
import configparser

import telegram




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

    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
    userWithCurrentChatAction = chat_id
    urlForCurrentChatAction = 'http://www.heavens-above.com/orbitdisplay.aspx?icon=iss&width=400&height=400&satid=25544'
    bot.sendPhoto(chat_id=userWithCurrentChatAction, photo=urlForCurrentChatAction,
                  caption='Current Position of the ISS')

plugin_info = {
    'name': "ISS",
    'desc': "Gets the position of the International Space Station."
}

arguments = {
    'text': [
        "(?i)^[\/](iss)"
    ]
}
