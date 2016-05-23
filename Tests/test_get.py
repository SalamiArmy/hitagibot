import json
import unittest
import plugins.get as get
import tgapi

class TestPick(unittest.TestCase):
    def test_get_admingroup(self):
        tg = tgapi.TelegramApi
        tg.message = json.loads("{\"message_id\":245,\"from\":{\"id\":33166369,\"first_name\":\"Ashley\",\"last_name\":\"Lewis\",\"username\":\"SalamiArmy\"},\"chat\":{\"id\":-55348600,\"title\":\"Donald Glover Appreciation\",\"type\":\"group\"},\"date\":1463933563,\"text\":\"\/get trippy swirl\",\"entities\":[{\"type\":\"bot_command\",\"offset\":0,\"length\":4}]}")
        tg.misc = json.loads("{\"bot_info\":{\"username\":\"@Bashs_Bot\"}}")
        result = get.main(tg)
        self.assertIn(result, ["jason", "justin", "mat"])

    # def test_get_botgroup(self):
    #     incomingMessage = json.loads("{\"misc\":{\"bot_info\":{\"username\":\"@Bashs_Bot\"}}, \"update_id\":709889770, \"message\":{\"message_id\":10970,\"from\":{\"id\":134480007,\"first_name\":\"Alex\",\"last_name\":\"Gaillard\",\"username\":\"Dusty_b\"},\"chat\":{\"id\":-1001048076684,\"title\":\"Jesus is my Homeboy\",\"type\":\"supergroup\"},\"date\":1463989697,\"text\":\"\/get dank memes\",\"entities\":[{\"type\":\"bot_command\",\"offset\":0,\"length\":4}]}}")
    #     result = get.main(incomingMessage)
    #     #self.assertIn(result, ["jason", "justin", "mat"])

if __name__ == "__main__":
    unittest.main()
