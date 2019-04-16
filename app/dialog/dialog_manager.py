import app.api.zalo_api as zaloAPI
import app.utils.utils_zalo as utils_zalo
import requests
import json
from app.dialog.trindikit import *
from flask import request, jsonify
from datetime import datetime
from app.dialog.dialog_utils import *
from app.dialog.handle_message import HandleMessage

class DialogManager:
  def __init__(self):
    self.DIALOGS = []
    self.handle_message = HandleMessage()

  def get_dialog_if_user_exist(self, user_id):
    if (len(self.DIALOGS) > 0):
      for dialog in self.DIALOGS:
        if user_id == dialog['user_id']:
          return dialog
    return None

  def reply(self):
    # reply = "Xin lỗi mình không trả lời được tin nhắn"
    user_id, user_msg, event = zaloAPI.receive_user_text()
    current_dialog = self.get_dialog_if_user_exist(user_id)
    if current_dialog == None:
      current_dialog = create_dialog(user_id)
      self.DIALOGS.append(current_dialog)

    print("Current DIALOGS: ", self.DIALOGS)

    if event == "sendmsg":
    # if isinstance(user_msg, str):
      current_dialog = self.handle_message.handle_message(user_msg, dialog = current_dialog)
      if current_dialog["responses"]["reply_type"] == "reply_text":
        zaloAPI.reply_user_text(user_id, current_dialog["responses"]["reply"])
      elif current_dialog["responses"]["reply_type"] == "reply_select":
        zaloAPI.reply_user_select_yes_no(user_id, current_dialog["responses"]["reply"], current_dialog["responses"]["sub_reply"], current_dialog["responses"]["image_url"])
      # elif current_dialog["responses"]["reply_type"] == "reply_link":

    if event == "order":
      order = json.loads(request.args.get('order'))
      time = datetime.fromtimestamp(int(order['createdTime'])/1000)
      reply = "Mã đơn hàng: " + order['orderCode'].upper() + "\nTổng thanh toán: " + str(int(order['price'])) + " đ\nNgày giờ đặt hàng: " + time.strftime('%H:%M %d/%m/%Y')
      # Reply with link
      links = [{
        'link': 'https://shop.zalo.me/profile/order_history?status=0',
        'linktitle': 'Đặt hàng thành công!',
        'linkdes': reply,
        'linkthumb': order['productImage']
      }]
      zaloAPI.reply_user_link(user_id, links)
      zaloAPI.reply_user_text(user_id,  "Cảm ơn bạn đã đặt hàng, chúc bạn ngon miệng!")
