from rivescript import RiveScript
import re
from app.clf.text_classifier_sklearn import TextClassificationPredict

bot = RiveScript(utf8=True)
bot.load_directory("engine/eg/brain")
bot.sort_replies()

class BotManager:
    def __init__(self, _isTest = False):
        self.isTest = _isTest

    @staticmethod
    def reply(msg):
        response = bot.reply("teabot", msg)
        if (response == "None"):
          clf_result = TextClassificationPredict(msg).get_train_data()
          clf_result.append(msg)
          return ', '.join(clf_result)
        else:
          return response
