# Hitagibot

Hitagi is a plugin based Telegram bot written in Python 3 and licensed under the GNU Affero General Public License
v3. The bot focuses on providing a lightweight and high performance modular environment for bot creation.

## Installation
You will need python 3 (3.5.1 is recommended) to use the bot.

First clone and cd to the repository
```bash
git clone https://github.com/TopBakuhatsu/hitagibot.git
cd hitagibot
```
Afterwards set your token in the config.ini.template and rename to config.ini
```
token = YOUR TOKEN HERE
```

Now you can start the bot with `./hitagi.py`. However the default configuration is very bare-bones. Head to the wiki to
learn more about plugin creation.


*Note:* In some cases you may also need to install requests, `pip3 install requests` or `easy_install3 requests`.


## What can it do?
| Method               | Status |
| -------------------- | ------ |
| getMe                | ✔      |
| sendMessage          | ✔      |
| forwardMessage       | ✔      |
| sendPhoto            | ✔      |
| sendAudio            | ✔      |
| sendDocument         | ✔      |
| sendSticker          | ✔      |
| sendVideo            | ✔      |
| sendVoice            | ✔      |
| sendLocation         | ✔      |
| SendVenue            | ✔      |
| SendContact          | ✔      |
| sendChatActions      | ✔      |
| getUserProfilePhotos | ✔      |
| getFile              | ✔      |
| kickChatMember       | ✔      |
| unbanChatMember      | ✔      |
| answerCallbackQuery  | ✔      |
| Updating Messages    | ✔      |
| Inline Mode          | ✖      |

