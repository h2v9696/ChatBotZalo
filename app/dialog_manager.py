import app.zalo_api as zaloAPI
from app.engine.main_bot import BotManager
from rivescript import RiveScript
import requests
from flask import request, jsonify
import json
from datetime import datetime

class DialogManager:
  def __init__(self):
    # self.bot = BotManager(True)
    self.bot = BotManager()
    self.riveBot = RiveScript(utf8=True)
    self.riveBot.load_directory("engine/eg/brain")
    self.riveBot.sort_replies()

  def reply(self):
    reply = "Xin lỗi mình không trả lời được tin nhắn"
    user_id, user_msg, event = zaloAPI.receive_user_text()
    if event == "sendmsg":
    # if isinstance(user_msg, str):
      user_msg = user_msg.replace('\n', ' ')
      user_msg = user_msg.replace(r'/', ' ')
      response = self.riveBot.reply("teabot", user_msg)
      if (response == "None"):
        intents, entities = self.bot.bot_process(user_msg)
        print(intents, entities)
        reply = self.simple_dialog(user_id, intents, entities)
      else:
        reply = response
    if event == "order":
      order = json.loads(request.args.get('order'))
      time = datetime.fromtimestamp(int(order['createdTime'])/1000)
      reply = "Mã đơn hàng: " + order['orderCode'] + "\nTổng thanh toán: " + str(int(order['price'])) + "đ\nNgày giờ đặt hàng: " + time.strftime('%H:%M %d/%m/%Y') + "\nCảm ơn bạn đã đặt hàng, chúc bạn ngon miệng!"
    return zaloAPI.reply_user_text(user_id, reply)

  def simple_dialog(self, user_id, intents, entities):
    result = "Xin lỗi mình không trả lời được tin nhắn"
    question_type = intents[0]
    domain = intents[1]
    question_attr = intents[2]
    userProfile = zaloAPI.get_user_profile(user_id)
    # print(userProfile)
    order = {
      'customer':
      {
          'name': userProfile['data']['displayName'],
          'phone': '',
          'user_id': userProfile['data']['userId'],
          'address': '',
          'district': 2,
          'city': 1
      },
      'order_items': [],
      'extra_note': "Ghi chú từ khách hàng: "
    }
    # Order product section
    if (question_type == "order" and domain == "product"):
      address = []
      index = 0
      for e in entities:
        if (entities.index(e) == index):
          if (e['type'] == 'TYPE'):
            extra_note = []
            item = {
              'product_id': '',
              'product_name': '',
              'quantity': 1,
              'variation':
              {
                'id': ''
              }
            }
            # Get product 'QUANTITY' if dont have 'QUANTITY' before that then dafault = 1
            if (index != 0):
              if (entities[index - 1]['type'] == 'QUANTITY'):
                item['quantity'] = int(entities[index - 1]['text'])
            # Get all 'TYPE' stand together
            product = []
            product.append(e['text'])
            if (index < len(entities) - 1):
              while (entities[index + 1]['type'] == 'TYPE'):
                product.append(entities[index + 1]['text'])
                e = entities[index + 1]
                index += 1
              item['product_name'] = ' '.join(product)
            # Get 'SIZE' 'TOPPING' 'ADJUSTICE' 'ADJUSTSUGAR' behind TYPE
            size = ""
            extra_note.append(item['product_name'])
            if (index < len(entities) - 1):
              while (entities[index + 1]['type'] == 'SIZE'
                        or entities[index + 1]['type'] == 'TOPPING'
                        or entities[index + 1]['type'] == 'ADJUSTICE'
                        or entities[index + 1]['type'] == 'ADJUSTSUGAR'):
                if entities[index + 1]['type'] == 'SIZE':
                  item['variation']['id'] = zaloAPI.convert_id_size(entities[index + 1]['text'])
                if entities[index + 1]['type'] == 'TOPPING':
                  extra_note.append("Topping: " + entities[index + 1]['text'].replace("_", " "))
                  # Order Topping
                  topping_item = {
                    'product_id': '',
                    'product_name': entities[index + 1]['text'].replace("_", " "),
                    'quantity': item['quantity'],
                  }
                  order['order_items'].append(topping_item)
                if entities[index + 1]['type'] == 'ADJUSTICE':
                  extra_note.append("Lượng đá: " + entities[index + 1]['text'])
                if entities[index + 1]['type'] == 'ADJUSTSUGAR':
                  extra_note.append("Lượng đường: " + entities[index + 1]['text'])
                e = entities[index + 1]
                index += 1
            # Append to order
            if (len(extra_note) != 0):
              order['extra_note'] += ', '.join(extra_note) + '; '
            order['order_items'].append(item)

          if (e['type'] == 'LOCATION'):
            address.append(e['text'].replace('_', ' '))

          if (e['type'] == 'PHONE'):
            order['customer']['phone'] = e['text']

          index += 1

      order['customer']['address'] = ' - '.join(address)
      # Get product id to complete order
      for item in order['order_items']:
        product = zaloAPI.get_product(item['product_name'])
        if 'variations' in product:
          for v in product['variations']:
            if item['variation']['id'] == '' and zaloAPI.convert_id_size(v['attributes'][0]) == 'm':
              item['variation']['id'] = v['id']
              break
            if v['attributes'][0] == item['variation']['id']:
              item['variation']['id'] = v['id']
        item['product_id'] = product["id"]
        item['product_name'] = product["name"]
      print(order)

      response = zaloAPI.create_order(order)
      if (response['error'] != 0):
        result = "Xin lỗi bạn quá trình order đã gặp vấn đề: " + response['message'] + "\nXin bạn thử lại sau."
      else:
        result = "Mình đã tạo order rồi nhé, mời bạn kiểm tra."
    return result
