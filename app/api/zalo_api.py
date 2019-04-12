from zalo.sdk.oa import ZaloOaInfo, ZaloOaClient
from zalo.sdk.store import ZaloStoreClient
from zalo.sdk.ZaloBaseClient import ZaloBaseClient
import json
from app.config import OAID, SECRET_KEY, ACCESS_TOKEN, API_URL
import app.utils.utils_zalo as utils_zalo
from flask import request, jsonify
import requests

zalooa_info = ZaloOaInfo(oa_id=OAID, secret_key=SECRET_KEY)
zalo_store_client = ZaloStoreClient(zalooa_info)
zalo_oa_client = ZaloOaClient(zalooa_info)

def receive_user_text():
  msg = request.args.get('message')
  user_id = request.args.get('fromuid')
  event = request.args.get('event')
  return user_id, msg, event

def reply_user_text(user_id, msg: str):
  data = {
      'uid': user_id,
      'message': msg
  }
  params = {'data': data}
  send_text_message = zalo_oa_client.post('sendmessage/text', params)
  return msg

def reply_user_link(user_id, links: list):
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

def create_order(order_info: dict):
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

def get_products(isGetMenu: bool = True):
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
    if (utils_zalo.get_category_from_id(categories, id = p['categories'][0]) == "Đồ uống"):
      drink.append(p)
    if (utils_zalo.get_category_from_id(categories, id = p['categories'][0]) == "Topping"):
      topping.append(p)
    all_products.append(p)
  # Show menu
  result = "Đồ uống\n"
  index = 1
  for d in drink:
    result += utils_zalo.print_product(index = index, products = d)
    index += 1
  result += "Topping\n"
  index = 1
  for t in topping:
    result += utils_zalo.print_product(index = index, products = t)
    index += 1
  if (isGetMenu):
    reply_user_text(user_id, result)
    return "Mời bạn chọn món!"

  return all_products

