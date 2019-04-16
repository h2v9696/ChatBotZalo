from app.dialog.handle_detail import HandleDetail
from app.utils.sentences import OTHER
from app.utils.get_random_reply import get_random_reply
from app.dialog.dialog_utils import *
from app.dialog.const import START_STATE, ORDERED_STATE, ORDERING_STATE

class HandleState:
  def __init__(self):
    self.handle_detail = HandleDetail()

  def handle_state(self, dialog: dict):
    """
    generation response by intent
    :param dialog: dict
    :return:
    """

    def apply_function(_state, _dialog):
      functions = {
        #order context
        ORDERING_STATE: self.__order_product,
        ORDERED_STATE: self.__order_product_confirm,

        #begin
        "begin": self.__begin
      }
      if (_state in functions):
        return functions[_state](state = _state, dialog=_dialog)
      return None

    state = dialog["state"]
    return apply_function(state, dialog)
    # If dont get user intent then reply OTHER
    # response = {
    #   "reply_type": "reply_text",
    #   "reply": get_random_reply(replies = OTHER)
    # }
    # _dialog = set_response(dialog = _dialog, response = response)
    # return _dialog

  def __begin(self, state: str, dialog: dict):
    # If state is "begin" then pass to handle with intent
    return None

  def __order_product(self, state: str, dialog: dict):
    """
    handle order_product by state (in a intent context)
    :param state:
    :param dialog:
    :return dialog:
    """

    dialog = self.handle_detail.order_product(dialog = dialog, state = state)
    return dialog

  def __order_product_confirm(self, state: str, dialog: dict):
    """
    handle order_product by state (in a intent context)
    :param state:
    :param dialog:
    :return dialog:
    """

    dialog = self.handle_detail.order_product_confirm(dialog = dialog, state = state)
    return dialog
