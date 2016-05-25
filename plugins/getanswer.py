import configparser

import tungsten as tungsten

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

    client = tungsten.Tungsten(keyConfig.get('Wolfram', 'WOLF_APP_ID'))
    result = client.query(requestText)
    if len(result.pods) >= 1:
        fullAnswer = ''
        for pod in result.pods:
            for answer in pod.format['plaintext']:
                if not answer == None:
                    fullAnswer += answer
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        return bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + fullAnswer)
    
    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    return bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                              ', I\'m afraid I can\'t find any answers for ' + \
                              requestText)

plugin_info = {
    'name': "Answer",
    'desc': "Gets an answer from Wolfram Alpha's Answers API."
}

arguments = {
    'text': [
        "(?i)^[\/](getanswer) (.*)"
    ]
}
