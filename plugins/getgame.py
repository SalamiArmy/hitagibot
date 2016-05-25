# coding=utf-8
import configparser
import urllib

import telegram
from bs4 import BeautifulSoup


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

    code = urllib.request.urlopen("http://store.steampowered.com/search/?term=" + requestText).read().decode('utf-8')
    appId = steam_results_parser(code)
    if appId:
        steamGameLink = "http://store.steampowered.com/app/" + appId
        bypassAgeGate = urllib.request.build_opener()
        bypassAgeGate.addheaders.append(('Cookie', 'birthtime=578390401'))
        code = bypassAgeGate.open(steamGameLink).read()
        # code = urllib.urlopen(steamGameLink).read()
        gameResults = steam_game_parser(code, steamGameLink)
    else:
        gameResults = ""
    if gameResults:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        return bot.sendMessage(chat_id=chat_id, text=gameResults,
                               disable_web_page_preview=True, parse_mode='Markdown')

    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    return bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                                 ', I\'m afraid I can\'t find the steam game ' + \
                                                 requestText)

def steam_results_parser(code):
    soup = BeautifulSoup(code, "html.parser")
    resultList = []
    for resultRow in soup.findAll("a", attrs={"class":"search_result_row"}):
        if "data-ds-appid" in resultRow.attrs:
            resultList.append(resultRow["data-ds-appid"])
        if "data-ds-bundleid" in resultRow.attrs:
            resultList.append(resultRow["data-ds-bundleid"])
    if len(resultList) > 0:
        return resultList[0]
    return ""

def steam_game_parser(code, link):
    soup = BeautifulSoup(code, "html.parser")
    AllGameDetailsFormatted = ""

    titleDiv = soup.find("div", attrs={"class":"apphub_AppName"})
    if titleDiv:
        gameTitle = titleDiv.string
        AllGameDetailsFormatted += "*" + gameTitle + "*" + "\n"

    descriptionDiv = soup.find("div", attrs={"class":"game_description_snippet"})
    if descriptionDiv:
        descriptionSnippet = descriptionDiv.string.replace("\r", "").replace("\n", "").replace("\t", "")
        AllGameDetailsFormatted += descriptionSnippet + "\n"

    if AllGameDetailsFormatted:
        AllGameDetailsFormatted += link + "\n"

    dateSpan = soup.find("span", attrs={"class":"date"})
    if dateSpan:
        releaseDate = dateSpan.string
        AllGameDetailsFormatted += "Release Date: " + releaseDate + "\n"

    featureList = ""
    featureLinks = soup.findAll("a", attrs={"class":"name"})
    if len(featureLinks) > 0:
        for featureLink in featureLinks:
            featureList += "     " + featureLink.string.replace("Seated", "Will make you shit yourself") + "\n"
        AllGameDetailsFormatted += "Features:\n" + featureList

    reviewRows = ""
    reviewDivs = soup.findAll("div", attrs={"class":"user_reviews_summary_row"})
    if len(reviewDivs) > 0:
        for reviewRow in reviewDivs:
            reviewSubtitleDiv = reviewRow.find("div", attrs={"class":"subtitle column"}).string
            reviewSummaryDiv = reviewRow.find("div", attrs={"class":"summary column"}).string
            if not reviewSummaryDiv:
                reviewSummaryDiv = reviewRow.find("span", attrs={"class":"nonresponsive_hidden responsive_reviewdesc"}).string
            reviewSummaryDiv = reviewSummaryDiv.replace("\r", "").replace("\n", "").replace("\t", "")
            if reviewSummaryDiv != "No user reviews":
                reviewRows += "     " + reviewSubtitleDiv + reviewSummaryDiv.replace("-", "").replace(" user reviews", "").replace(" of the ", " of ") + "\n"
        if reviewRows:
            AllGameDetailsFormatted += "Reviews:\n" + reviewRows
        if AllGameDetailsFormatted.endswith("\n"):
            AllGameDetailsFormatted = AllGameDetailsFormatted[:AllGameDetailsFormatted.rfind("\n")]

    tagList = ""
    tagLinks = soup.findAll("a", attrs={"class":"app_tag"})
    if len(tagLinks) > 0:
        for tagLink in tagLinks:
            tagList += tagLink.string.replace("\r", "").replace("\n", "").replace("\t", "") + ", "
        AllGameDetailsFormatted += "\n" + "Tags:\n`" + tagList
    if AllGameDetailsFormatted.endswith(", "):
        AllGameDetailsFormatted = AllGameDetailsFormatted[:AllGameDetailsFormatted.rfind(", ")]
        AllGameDetailsFormatted += "`"

    return AllGameDetailsFormatted

plugin_info = {
    'name': "Game",
    'desc': "Gets game info from the Steam store."
}

arguments = {
    'text': [
        "(?i)^[\/](getgame) (.*)"
    ]
}
