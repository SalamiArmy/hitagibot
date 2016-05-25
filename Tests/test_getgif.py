import configparser
import json
import unittest
import plugins.getgif as getgif
import tgapi

class TestPick(unittest.TestCase):
    def test_getgif(self):
        tg = tgapi.TelegramApi
        fullMessageText = '/getgif trippy swirl'

        keyConfig = configparser.ConfigParser()
        keyConfig.read(["keys.ini", "config.ini", "..\keys.ini", "..\config.ini"])
        chatId = keyConfig['BOT_CONFIG']['admins']

        #for bot group:
        #chatId = -1001048076684

        tg.message = json.loads(
            "{\"message_id\":245,\"from\":{\"id\":33166369,\"first_name\":\"Ashley\",\"last_name\":\"Lewis\",\"username\":\"SalamiArmy\"},\"chat\":{\"id\":" + str(
                chatId) + ",\"title\":\"Donald Glover Appreciation\",\"type\":\"group\"},\"date\":1463933563,\"text\":\"" + fullMessageText +
            "\",\"entities\":[{\"type\":\"bot_command\",\"offset\":0,\"length\":4}]}")
        tg.misc = json.loads("{\"bot_info\":{\"username\":\"@Bashs_Bot\"}}")
        result = getgif.main(tg)
        self.assertIsNotNone(result, 'No result returned.')

if __name__ == "__main__":
    unittest.main()
