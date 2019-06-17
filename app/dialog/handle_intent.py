from app.dialog.handle_detail import HandleDetail
from app.utils.sentences import OTHER, CALL_BOSS
from app.utils.sentence_utils import *
from app.dialog.dialog_utils import *
from app.dialog.const import ORDER_INTENT, EXIST_INTENT, SENTIMENT_INTENT, ASK_PRICE_INTENT, \
  ASK_TIME_INTENT, ASK_LOC_INTENT, YESNO_PRODUCT_INTENT, YESNO_SHIP_INTENT, PROMOTION_INTENT, \
  ASK_PRODUCT_SIZE_INTENT, START_STATE, ASK_PHONE_INTENT

class HandleIntent:
  def __init__(self):
    self.handle_detail = HandleDetail()

  def handle_intent(self, dialog: dict):
    """
    generation response by intent
    :param dialog: dict
    :return:
    """

    def apply_function(_intent, _dialog):
      functions = {
        ORDER_INTENT: self.__order_product,
        EXIST_INTENT: self.__exist_product,
        SENTIMENT_INTENT: self.__handle_sentiment,
        ASK_PRICE_INTENT: self.__handle_ask_price,
        ASK_TIME_INTENT: self.__handle_ask_simple_answer,
        ASK_LOC_INTENT: self.__handle_ask_simple_answer,
        YESNO_SHIP_INTENT: self.__handle_ask_simple_answer,
        PROMOTION_INTENT: self.__handle_ask_simple_answer,
        ASK_PHONE_INTENT: self.__handle_ask_simple_answer,
        ASK_PRODUCT_SIZE_INTENT: self.__handle_ask_simple_answer,
        YESNO_PRODUCT_INTENT: self.__handle_yesno_product,
      }
      if (_intent in functions):
        return functions[_intent](intent = _intent, dialog = _dialog)

      if (_dialog['failTimes'] < 2):
        reply = get_random_reply(replies = OTHER)
      else:
        reply = get_random_reply(replies = CALL_BOSS)
        _dialog['failTimes'] = 0

      # If dont get user intent then reply OTHER
      response = {
        "reply_type": "reply_text",
        "reply": reply
      }
      if get_state(dialog = _dialog) == START_STATE:
        _dialog['failTimes'] += 1
      else:
        _dialog['failTimes'] = 0
      _dialog = set_response(dialog = _dialog, response = response)
      return _dialog

    intent = dialog["snips"]["intent"]
    return apply_function(intent, dialog)

  def __order_product(self, intent: str, dialog: dict):
    """
    handle order_product by intent
    :param intent:
    :param dialog:
    :return:
    """

    dialog = self.handle_detail.order_product(dialog = dialog, state = (intent + "_ing"))
    return dialog

  def __exist_product(self, intent: str, dialog: dict):
    """
    handle exist_product by intent
    :param intent:
    :param dialog:
    :return:
    """

    dialog = self.handle_detail.exist_product(dialog = dialog, state = (intent + "_ing"))
    return dialog

  def __handle_sentiment(self, intent: str, dialog: dict):
    """
    handle sentiment by intent
    :param intent:
    :param dialog:
    :return:
    """

    dialog = self.handle_detail.handle_sentiment(dialog = dialog, state = (intent + "_ing"))
    return dialog

  def __handle_ask_price(self, intent: str, dialog: dict):
    """
    handle ask price by intent
    :param intent:
    :param dialog:
    :return:
    """

    dialog = self.handle_detail.handle_ask_price(dialog = dialog, state = (intent + "_ing"))
    return dialog

  def __handle_ask_simple_answer(self, intent: str, dialog: dict):
    """
    handle ask simple answer by intent
    :param intent:
    :param dialog:
    :return:
    """

    dialog = self.handle_detail.handle_ask_simple_answer(dialog = dialog, state = (intent + "_ing"))
    return dialog

  def __handle_yesno_product(self, intent: str, dialog: dict):
    """
    handle yes no product by intent
    :param intent:
    :param dialog:
    :return:
    """

    dialog = self.handle_detail.handle_yesno_product(dialog = dialog, state = (intent + "_ing"))
    return dialog

