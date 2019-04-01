from rivescript import RiveScript
import re
from app.clf.text_classifier_sklearn import TextClassificationPredict
from app.ner.src.neuroner import NeuroNER

bot = RiveScript(utf8=True)
bot.load_directory("engine/eg/brain")
bot.sort_replies()

# nn = NeuroNER(parameters_filepath = "ner/src/parameters.ini")

class BotManager:
    def __init__(self, _isTrain = False):
        self.ner = NeuroNER(parameters_filepath = "ner/src/parameters.ini",
                                          train_model = _isTrain,
                                          use_pretrained_model = not _isTrain,
                                          pretrained_model_folder = "ner/trained_models/vi_2019-03-31")
        self.isTrain = _isTrain

    def reply(self, msg):
        if not isinstance(msg, str):
          return None
        msg = msg.replace('\n', ' ')
        response = bot.reply("teabot", msg)
        if (response == "None"):
          result = 'Intent:\n\t'
          intents = self.getIntent(msg)
          # intents = TextClassificationPredict(msg).get_train_data()
          s = ', '.join(intents)
          result += s + '\n'
          # pre-process for ner
          msg = self.preProcessLoc(msg.lower())
          numbers = []
          numbers, msg = self.preProcessNumber(msg)
          # print(numbers, msg)

          entities = self.getNER(msg)
          # entities = nn.predict(text=msg)
          result += "NER:\n"
          count = 0
          for e in entities:
            if (count < len(numbers)):
              if ("number" in e['text']):
                e['text'] = e['text'].replace('number', numbers[count])
                count += 1
              elif ("phone" in e['text']):
                while len(numbers[count]) <= 9:
                  count += 1
                e['text'] = e['text'].replace('phone', numbers[count])
                count += 1
            # fail
            s = '\t' + e['text'] + ' = ' + e['type'] + '\n'
            result += s
          print(entities)
          return result + self.preProcessLoc(msg.lower())
        else:
          return response

    def getIntent(self, msg):
      return TextClassificationPredict(msg).get_train_data()

    def getNER(self, msg):
      # nn = NeuroNER(parameters_filepath = "ner/src/parameters.ini")
      if self.isTrain:
        self.ner.fit()
      return self.ner.predict(text=msg)

    def preProcessLoc(self, msg):
      f = open("ner/data/dic_location", "r")
      if f.mode == 'r':
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            if line in msg:
              new_line = line.replace(' ', '_')
              msg = msg.replace(line, new_line)
      return msg

    def preProcessNumber(self, msg):
      #tiền xử lý
      msg = msg.replace("%", " %")
      msg = msg.replace("số điện thoại", "sdt")
      words = msg.split(' ')
      numbers = []
      processed_msg = []
      for word in msg.split(' '):
        if (word.isnumeric()):
          numbers.append(word)
          if (len(word) > 9):
            processed_msg.append("phone")
          else:
            processed_msg.append("number")
        else:
          processed_msg.append(word)
      return numbers, ' '.join(processed_msg)

      # for word in msg.split(' '):
      #   if (word.isnumeric()):
      #     numbers.append(word)
      # processed_msg = re.sub(r"\b\d+\b", "number", msg)
      # return numbers, processed_msg
