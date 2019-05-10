import re
from app.clf.text_classifier_sklearn import TextClassificationPredict
from app.ner.src.neuroner import NeuroNER

EXCEPTION_WORD = ("chanh",)
# nn = NeuroNER(parameters_filepath = "ner/src/parameters.ini")

class BotManager:
    def __init__(self, _isTrain = False):
      # self.ner = None
      self.ner = NeuroNER(parameters_filepath = "ner/src/parameters.ini",
                                        train_model = _isTrain,
                                        use_pretrained_model = not _isTrain,
                                        pretrained_model_folder = "ner/trained_models/vi_2019-04-22")
      self.isTrain = _isTrain
      f = open("ner/data/dic_location", "r")
      self.location_dict = f.readlines()

    # Get intent and NER
    def bot_process(self, msg):
      intents = self.getIntent(msg)

      # pre-process for ner
      msg = self.preProcessLoc(msg.lower())
      numbers = []
      numbers, msg = self.preProcessNumber(msg)
      # print (numbers, msg)

      msg = self.fix_spacy_exception_after(msg)
      # print(numbers, msg)
      entities = self.getNER(msg)
      # Change number and phone back to it's original
      for number in numbers:
        for e in entities:
          # print(number['start'], e['text'], e['start'], '\n')
          if (e['start'] <= number['start'] and ('number' in e['text'] or 'phone' in e['text'])):
            e['text'] = e['text'].replace("number", number['word'])
            e['text'] = e['text'].replace("phone", number['word'])
            break
      #add LOCATION if cant catch
      for line in self.location_dict:
        line = line[:-1]
        is_existed = False
        line = line.replace(' ', '_')
        if line in msg:
          for e in entities:
            if line in e['text']:
              is_existed = True
          if not is_existed:
            new_entities = {'id': 'Tnew', 'type': 'LOCATION', 'start': len(msg) + 1, 'end': len(msg) + 1 + len(line), 'text': line}
            entities.append(new_entities)
      return intents, entities

    def getIntent(self, msg):
      return TextClassificationPredict(msg).get_train_data()

    def getNER(self, msg):
      # nn = NeuroNER(parameters_filepath = "ner/src/parameters.ini")
      if self.isTrain:
        self.ner.fit()
      return self.ner.predict(text=msg)

    def preProcessLoc(self, msg):
      for line in self.location_dict:
          line = line[:-1]
          if line in msg:
            new_line = line.replace(' ', '_')
            msg = msg.replace(line, new_line)
      return msg

    def preProcessNumber(self, msg):
      #tiền xử lý
      msg = self.fix_spacy_exception(msg)
      words = msg.split(' ')
      numbers = []
      processed_msg = []
      start = 0
      for  i, word in enumerate(words):
        if (word.isnumeric()):
          number = {
            'start': start,
            'word': word
          }
          numbers.append(number)
          if (len(word) > 9):
            processed_msg.append("phone")
            start += 5
          else:
            processed_msg.append("number")
            start += 6
        else:
          processed_msg.append(word)
          start += len(word)
          # if (word in EXCEPTION_WORD):
          #   start += 2
        start += 1 #space
      return numbers, ' '.join(processed_msg)

    def fix_spacy_exception(self, msg):
      msg = msg.replace("%", " %")
      msg = msg.replace(",", " ,")
      msg = msg.replace("số điện thoại", "sdt")
      msg = msg.replace("l nhé", "l")
      msg = msg.replace("l đi", "l")
      msg = msg.replace("chanh nhé", "chanh")
      msg = msg.replace("chanh thạch", "chanh , thạch")
      msg = msg.replace("chanh cỡ", "chanh , cỡ")
      msg = msg.replace("chanh loại", "chanh , loại")
      msg = msg.replace("chanh đi", "chanh")
      msg = msg.replace("chanh thôi", "chanh")
      msg = msg.replace("chanh size", "chanh , size")
      msg = msg.replace("cẩm thạch", "cẩm , thạch")
      msg = msg.replace("l vậy", "l")
      msg = msg.replace("l thạch", "l , thạch")
      return msg

    def fix_spacy_exception_after(self, msg):
      msg = msg.replace("chanh number", "chanh , number")
      return msg

