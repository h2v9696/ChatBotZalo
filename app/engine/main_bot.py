from rivescript import RiveScript
import re
from app.clf.text_classifier_sklearn import TextClassificationPredict
from app.ner.src.neuroner import NeuroNER

bot = RiveScript(utf8=True)
bot.load_directory("engine/eg/brain")
bot.sort_replies()

nn = NeuroNER(parameters_filepath = "ner/src/parameters.ini")

class BotManager:
    def __init__(self, _isTest = False):
        self.isTest = _isTest

    @staticmethod
    def reply(msg):
        response = bot.reply("teabot", msg)
        if (response == "None"):
          result = 'Intent:\n\t';
          clf_result = TextClassificationPredict(msg).get_train_data()
          s = ', '.join(clf_result)
          result += s + '\n'

          # nn = NeuroNER(parameters_filepath = "ner/src/parameters.ini")
          # nn.fit()
          entities = nn.predict(text=msg)
          result += "NER:\n"
          for e in entities:
            s = '\t' + e['text'] + ' : ' + e['type'] + '\n'
            result += s
          return result
        else:
          return response
