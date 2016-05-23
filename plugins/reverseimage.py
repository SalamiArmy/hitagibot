# coding=utf-8
import configparser
import logging

import telegram
# reverse image search imports:
import io
import pycurl, json
import certifi


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

    returned_code = io.StringIO()
    full_url = "https://www.google.com/searchbyimage?&image_url=" + requestText
    conn = pycurl.Curl()
    conn.setopt(conn.URL, str(full_url))
    conn.setopt(conn.CAINFO, certifi.where())
    conn.setopt(conn.FOLLOWLOCATION, 1)
    conn.setopt(conn.USERAGENT, "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11")
    conn.setopt(conn.WRITEFUNCTION, returned_code.write)
    conn.perform()
    conn.close()
    jsonResults = json.loads(returned_code.getvalue())
    resultsText = ''
    if 'result_qty' in jsonResults and len(jsonResults['result_qty']) > 0:
        for jsonResult in jsonResults['result_qty']:
            resultsText += jsonResult + '\n'
    if 'title' in jsonResults and len(jsonResults['title']) > 0:
        for jsonResult in jsonResults['title']:
            resultsText += jsonResult + '\n'
    if 'description' in jsonResults and len(jsonResults['description']) > 0:
        for jsonResult in jsonResults['description']:
            resultsText += (jsonResult[jsonResult.index('-') + 2:] + '\n' if '-' in jsonResult else '')
    if 'links' in jsonResults and len(jsonResults['links']) > 0:
        for jsonResult in jsonResults['links']:
            resultsText += jsonResult + '\n'
    resultLinks = code[code.index('Search Results'):].split('href=')
    for resultLink in resultLinks[1:]:
        resultLink = resultLink[1:]
        foundLink = resultLink[:resultLink.index('"')]
        if foundLink != '#' and \
                        foundLink != 'javascript:;' and \
                        foundLink != 'javascript:void(0)' and \
                        foundLink != '//www.google.com/intl/en/policies/privacy/?fg=1' and \
                        foundLink != '//www.google.com/intl/en/policies/terms/?fg=1' and \
                        len(foundLink) < 50:
            resultsText += foundLink + '\n'
    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    userWithCurrentChatAction = chat_id
    urlForCurrentChatAction = resultsText
    bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)

plugin_info = {
    'name': "Reverse Image",
    'desc': "Gets reverse image search results from Google Images."
}

arguments = {
    'text': [
        "^[/](reverseimage) (.*)"
    ]
}
