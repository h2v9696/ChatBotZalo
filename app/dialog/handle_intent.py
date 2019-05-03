from app.dialog.handle_detail import HandleDetail
from app.utils.sentences import OTHER
from app.utils.sentence_utils import *
from app.dialog.dialog_utils import *
from app.dialog.const import ORDER_INTENT, EXIST_INTENT

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
      }
      if (_intent in functions):
        return functions[_intent](intent = _intent, dialog = _dialog)

      # If dont get user intent then reply OTHER
      response = {
        "reply_type": "reply_text",
        "reply": get_random_reply(replies = OTHER)
      }
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
