from zalo.sdk.oa import ZaloOaInfo, ZaloOaClient
from zalo.sdk.store import ZaloStoreClient
from zalo.sdk.ZaloBaseClient import ZaloBaseClient
import json
from app.config import OAID, SECRET_KEY, ACCESS_TOKEN, API_URL
from flask import request, jsonify
from zalo.sdk.APIException import APIException
import requests

zalooa_info = ZaloOaInfo(oa_id=OAID, secret_key=SECRET_KEY)
zalo_store_client = ZaloStoreClient(zalooa_info)
zalo_oa_client = ZaloOaClient(zalooa_info)

def receive_user_text():
  msg = request.args.get('message')
  user_id = request.args.get('fromuid')
  event = request.args.get('event')
  return user_id, msg, event

def reply_user_text(user_id, msg):
  data = {
      'uid': user_id,
      'message': msg
  }
  params = {'data': data}
  send_text_message = zalo_oa_client.post('sendmessage/text', params)
  return msg

def reply_user_link(user_id, links):
  data = {
      'uid': user_id,
      'links': links
  }
  params = {
      'data': data
  }
  send_link_message = zalo_oa_client.post('sendmessage/links', params)
  print(send_link_message)

  return links

def get_user_profile(user_id):
  return zalo_oa_client.get('getprofile', {'uid': user_id})

def create_order(order_info):
  response = requests.post(url= API_URL +"store/order/create?access_token=" + ACCESS_TOKEN,
    json=order_info)
  print(response.json())
  return response.json()

def get_category():
  offset = 0
  limit = 10
  response = requests.get(url= API_URL +"store/category/getcategoryofoa?access_token="
   + ACCESS_TOKEN + "&offset=" + str(offset) + "&limit=" + str(limit))
  # print(response.json())
  return response.json()['data']['categories']

def get_products(isGetMenu = True):
  user_id, msg, event = receive_user_text()
  categories = get_category()

  all_products = []
  drink = []
  topping = []
  # Request get all products
  offset = 0
  limit = 50
  response = requests.get(url= API_URL +"store/product/getproductofoa?access_token="
   + ACCESS_TOKEN + "&offset=" + str(offset) + "&limit=" + str(limit))
  get_list_product = response.json()
  # Get product data
  for p in reversed(get_list_product['data']['products']):
    if (get_category_from_id(p['categories'][0], categories) == "Đồ uống"):
      drink.append(p)
    if (get_category_from_id(p['categories'][0], categories) == "Topping"):
      topping.append(p)
    all_products.append(p)
  # Show menu
  result = "Đồ uống\n"
  index = 1
  for d in drink:
    result += print_product(index, d)
    index += 1
  result += "Topping\n"
  index = 1
  for t in topping:
    result += print_product(index, t)
    index += 1
  if (isGetMenu):
    reply_user_text(user_id, result)
    return "Mời bạn chọn món!"

  return all_products

def get_product(product_name_from_user = ""):
  all_products = get_products(False)
  # print(all_products)
  product_name_from_user = product_name_from_user.replace("_", " ")
  if (len(all_products) != 0):
    for p in all_products:
      if product_name_from_user in p['name'].lower():
        return p
  return None

def convert_id_size(string = ""):
  string = string.lower()
  if (string == '1803545c6c198547dc08'):
    return 'm'
  elif (string == 'fcb7b1e889ad60f339bc'):
    return 'l'
  elif (string == 'm'):
    return '1803545c6c198547dc08'
  elif (string == 'l'):
    return 'fcb7b1e889ad60f339bc'

def get_category_from_id(string, categories):
  for c in categories:
    if (string == c['id']):
      return c['name']

def print_product(index, p):
  if 'variations' not in p:
    return "{:<2}\t{:<} - {:<}".format(str(index),p['name'],str(p['price'])) + "đ\n"
  else:
    m_price = 0
    l_price = 0
    for v in p['variations']:
      if convert_id_size(v['attributes'][0]) == 'm':
        m_price = "M: " + str(int(v['price'])) + "đ"
      if convert_id_size(v['attributes'][0]) == 'l':
        l_price = "L: " + str(int(v['price'])) + "đ\n"
    return "{:<2}\t{:<} - {:<} - {:<}".format(str(index),p['name'], m_price, l_price)
