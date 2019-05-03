from app.engine.main_bot import BotManager
from rivescript import RiveScript
from app.dialog.dialog_utils import *
from app.dialog.handle_intent import HandleIntent
from app.dialog.handle_state import HandleState
from app.dialog.const import START_STATE, ORDER_INTENT, ORDERING_STATE, EXIST_INTENT, SENTIMENT_INTENT
import json
import app.utils.utils_zalo as utils_zalo
from app.utils.sentences import WAIT_PROCESS_ORDER
from app.utils.sentence_utils import *
import app.api.zalo_api as zaloAPI



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
    user_msg = self.pre_process(msg = user_msg)
    # reply = "Xin lỗi mình không trả lời được tin nhắn"
    response = {
        "reply_type": "reply_text",
        "reply": "None"
    }
    if get_state(dialog) == START_STATE:
      response = {
        "reply_type": "reply_text",
        "reply": self.riveBot.reply("teabot", user_msg)
      }
    if (response['reply'] == "None"):
      intents, entities = self.nlpBot.bot_process(user_msg)
      print("\nIntent, entities: ", intents, "\n", json.dumps(entities, indent = 2, ensure_ascii = False))

      # print(intents, entities)
      intent = self.convert_intents(intents)
      if (intent == ORDER_INTENT and get_state(dialog) == START_STATE):
        zaloAPI.reply_user_text(dialog['user_id'], get_random_reply(replies = WAIT_PROCESS_ORDER))
      entities = self.convert_entities(entities)
      # print("\nUpdated intent, entities: ", intent, entities)
      update_snips(dialog = dialog, msg = user_msg, intent = intent, entities = entities)
      print("\nUpdated dialog: ", json.dumps(dialog, indent = 2, ensure_ascii = False))

      #Check if dialog is in some state
      dialog_state = self.handle_state.handle_state(dialog)
      if dialog_state:
        return dialog_state

      dialog = self.handle_intent.handle_intent(dialog)
    else:
      set_response(dialog = dialog, response= response)


    return dialog

  def pre_process(self, msg: str):
    msg = msg.replace('\n', ' ')
    msg = msg.replace(r'/', ' ')
    # Temporary pre process these word
    msg = msg.replace("chân trâu", 'trân châu')
    msg = msg.replace("ô long", 'oolong')
    msg = msg.replace("cafe", 'cà phê')
    msg = msg.replace("coffee", 'cà phê')
    msg = msg.replace("coffe", 'cà phê')
    msg = msg.replace("sô cô la", 'chocolate')
    msg = msg.replace("sôcôla", 'chocolate')
    msg = msg.replace("cho co lát", 'chocolate')
    msg = msg.replace("trân châu đường đen", 'trân châu đen')

    return msg



#Utils
  def convert_intents(self, intents):
    """
    Convert 3 intents into 1 intent
    """
    question_type = intents[0]
    domain = intents[1]
    question_attr = intents[2]
    if (question_type == "order" and (domain == "product" or domain == "ship")):
      return ORDER_INTENT
    if (question_type == "exists" and domain == "product"):
      return EXIST_INTENT
    if (question_type == "sentiment"):
      return SENTIMENT_INTENT
    return None

  def convert_entities(self, entities):
    """
    Convert entities n "TYPE" > 1 "TYPE", n "LOCATION" > 1 "LOCATION" ...
    """
    for e in entities:
      e['text'] = e['text'].replace("_", " ")
    entities = self.merge_entity_by_type(entities, entity_type = "TYPE", delimiter = " ")
    entities = self.merge_entity_by_type(entities, entity_type = "LOCATION", delimiter = " ")

    return entities

  def merge_entity_by_type(self, entities, entity_type: str, delimiter: str):
    # Maybe replace "_" to  " "
    merge = ""
    all_products = zaloAPI.get_products(False)

    for index, entity in enumerate(entities):
      if (entity["type"] == entity_type):
        merge = entity['text']
        if (index < len(entities) - 1):
          i = index + 1
          while (entities[i]['type'] == entity_type):
            if (entity_type == "TYPE"):
              if (utils_zalo.get_product(all_products, merge + delimiter + entities[i]['text'], full_word = True)):
                merge += delimiter + entities[i]['text']
                entities.pop(i)
                # entities.remove(entities[i])
              else:
                i += 1
            else:
              merge += delimiter + entities[i]['text']
              entities.pop(i)
              # entities.remove(entities[i])
            if (i > len(entities) - 1):
                break
        entity["text"] = merge
    return entities
