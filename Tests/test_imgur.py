import json
import unittest
import plugins.igmur as igmur
import tgapi

class TestPick(unittest.TestCase):
    def test_get_admingroup(self):
        tg = tgapi.TelegramApi
        fullMessageText = '/imgur flail'
        chatId = -55348600

        #for bot group:
        #chatId = -1001048076684

        tg.message = json.loads("{\"message_id\":245,\"from\":{\"id\":33166369,\"first_name\":\"Ashley\",\"last_name\":\"Lewis\",\"username\":\"SalamiArmy\"},\"chat\":{\"id\":" + str(chatId) + ",\"title\":\"Donald Glover Appreciation\",\"type\":\"group\"},\"date\":1463933563,\"text\":\"" + fullMessageText + "\",\"entities\":[{\"type\":\"bot_command\",\"offset\":0,\"length\":4}]}")
        tg.misc = json.loads("{\"bot_info\":{\"username\":\"@Bashs_Bot\"}}")
        result = igmur.main(tg)
        self.assertIn(result, ["jason", "justin", "mat"])

if __name__ == "__main__":
    unittest.main()