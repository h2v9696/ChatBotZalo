from zalo.sdk.oa import ZaloOaInfo, ZaloOaClient
from zalo.sdk.store import ZaloStoreClient
import json
from app.config import OAID, SECRET_KEY
from app.engine.main_bot import BotManager
from flask import request, jsonify

class ZaloAPI:
  def __init__(self):
    self.zalooa_info = ZaloOaInfo(oa_id=OAID, secret_key=SECRET_KEY)
    self.zalo_oa_client = ZaloOaClient(self.zalooa_info)
    self.zalo_store_client = ZaloStoreClient(self.zalooa_info)
    # self.bot = BotManager(True)
    self.bot = BotManager()

  def reply(self):
    msg = request.args.get('message')
    user_id = request.args.get('fromuid')
    data = {
        'uid': user_id,
        'message': self.bot.reply(msg)
        # 'message': bot.reply(msg.lower())
        # 'message': 'Chào bạn ' + profile['data']['displayName']
    }
    params = {'data': data}
    send_text_message = self.zalo_oa_client.post('sendmessage/text', params)
    return msg

  def get_products(self):
    data = {
      'offset': 0,
      'count': 1
    }
    params = {'data': data}
    get_list_product = self.zalo_store_client.get('store/product/getproductofoa', params)
    data = {
      'offset': 0,
      'count': get_list_product['data']['total']
    }
    params = {'data': data}
    get_list_product = self.zalo_store_client.get('store/product/getproductofoa', params)
    i = 1
    s = ""
    for p in get_list_product['data']['products']:
      s += str(i) + ": " + p['name'] + "\n"
      i += 1
    return s
