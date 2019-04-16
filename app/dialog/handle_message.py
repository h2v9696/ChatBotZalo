from app.engine.main_bot import BotManager
from rivescript import RiveScript
from app.dialog.dialog_utils import *
from app.dialog.handle_intent import HandleIntent
from app.dialog.handle_state import HandleState
from app.dialog.const import START_STATE, ORDER_INTENT, ORDERING_STATE

#Utils
def convert_intents(intents):
  """
  Convert 3 intents into 1 intent
  """
  question_type = intents[0]
  domain = intents[1]
  question_attr = intents[2]
  if (question_type == "order" and (domain == "product" or domain == "ship")) :
    return ORDER_INTENT
  return None

def convert_entities(entities):
  """
  Convert entities n "TYPE" > 1 "TYPE", n "LOCATION" > 1 "LOCATION" ...
  """
  entities = merge_entity_by_type(entities, entity_type = "TYPE", delimiter = " ")
  entities = merge_entity_by_type(entities, entity_type = "LOCATION", delimiter = " ")

  return entities

def merge_entity_by_type(entities, entity_type: str, delimiter: str):
  # Maybe replace "_" to  " "
  index = 0
  for entity in entities:
    if (entity["type"] == entity_type):
      merge = []
      merge.append(entity['text'].replace("_", " "))
      if (index < len(entities) - 1):
        while (entities[index + 1]['type'] == entity_type):
          merge.append(entities[index + 1]['text'].replace("_", " "))
          entities.remove(entities[index + 1])
        entity["text"] = delimiter.join(merge)
    index += 1
  return entities

class HandleMessage:
  def __init__(self):
    # self.bot = BotManager(True)
    self.nlpBot = BotManager()
    self.riveBot = RiveScript(utf8=True)
    self.riveBot.load_directory("engine/eg/brain")
    self.riveBot.sort_replies()
    self.handle_intent = HandleIntent()
    self.handle_state = HandleState()

  def handle_message(self, user_msg, dialog: dict):
    """
    Handle user text message
    :param user_msg: str User message
    :param dialog: dict
    :return dialog: dict
    """
    user_msg = user_msg.replace('\n', ' ')
    user_msg = user_msg.replace(r'/', ' ')
    reply = "Xin lỗi mình không trả lời được tin nhắn"
    response = self.riveBot.reply("teabot", user_msg)
    if (response == "None"):
      intents, entities = self.nlpBot.bot_process(user_msg)
      print("\nIntent, entities: ", intents, entities)

      # print(intents, entities)
      intent = convert_intents(intents)
      entities = convert_entities(entities)
      print("\nUpdated intent, entities: ", intent, entities)
      update_snips(dialog = dialog, msg = user_msg, intent = intent, entities = entities)
      print("\nUpdated dialog: ", dialog)

      #Check xem co phai dang trong stat nao do khong
      dialog_state = self.handle_state.handle_state(dialog)
      if dialog_state:
        return dialog_state

      dialog = self.handle_intent.handle_intent(dialog)
    else:
      set_response(dialog = dialog, response= response)

    return dialog



