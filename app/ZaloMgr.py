from zalo.sdk.oa import ZaloOaInfo, ZaloOaClient
from zalo.sdk.store import ZaloStoreClient
import json
from app import config
from app.engine.main_bot import BotManager
from flask import request, jsonify

zalooa_info = ZaloOaInfo(oa_id=config.oaid, secret_key=config.secretKey)
zalo_oa_client = ZaloOaClient(zalooa_info)
zalo_store_client = ZaloStoreClient(zalooa_info)

def reply():
  msg = request.args.get('message')
  user_id = request.args.get('fromuid')
  data = {
      'uid': user_id,
      'message': BotManager.reply(msg.lower())
      # 'message': 'Chào bạn ' + profile['data']['displayName']
  }
  params = {'data': data}
  send_text_message = zalo_oa_client.post('sendmessage/text', params)
  return msg

def get_products():
  data = {
    'offset': 0,
    'count': 1
  }
  params = {'data': data}
  get_list_product = zalo_store_client.get('store/product/getproductofoa', params)
  data = {
    'offset': 0,
    'count': get_list_product['data']['total']
  }
  params = {'data': data}
  get_list_product = zalo_store_client.get('store/product/getproductofoa', params)
  i = 1
  s = ""
  for p in get_list_product['data']['products']:
    s += str(i) + ": " + p['name'] + "\n"
    i += 1
  return s
