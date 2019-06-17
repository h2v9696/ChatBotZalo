from zalo.sdk.oa import ZaloOaInfo, ZaloOaClient
from zalo.sdk.store import ZaloStoreClient
from zalo.sdk.ZaloBaseClient import ZaloBaseClient
import json
from app.config import OAID, SECRET_KEY, ACCESS_TOKEN, API_URL, FOOD_API_URL
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
  print("\nReply user by text: ", send_text_message)
  # return msg

def reply_user_link(user_id, links: list):
  data = {
      'uid': user_id,
      'links': links
  }
  params = {
      'data': data
  }
  send_link_message = zalo_oa_client.post('sendmessage/links', params)
  print("\nReply user by link: ", send_link_message)
  # return links

def reply_user_sticker(user_id, sticker_id: str):
  data = {
    'uid': user_id,
    'stickerid': sticker_id
  }
  params = {'data': data}
  send_sticker_message = zalo_oa_client.post('sendmessage/sticker', params)
  print("\nReply user by sticker: ", send_sticker_message)
  # return msg


def reply_user_select(user_id, msg: str, sub_msg: str, img_url: str):
  message_info = {
    'recipient': {
      'user_id': user_id
    },
    'message': {
      'attachment': {
        'type': "template",
        'payload': {
          "template_type": "list",
          "elements": [{
            "title": msg,
            "subtitle": sub_msg,
            "image_url": img_url
          }],
          "buttons": [
           {
              "title": "Xác nhận",
              "payload": "Xác nhận",
              "type": "oa.query.show"
           },
           {
              "title": "Đổi món",
              "payload": "Đổi",
              "type": "oa.query.show"
           },
           {
              "title": "Thêm món",
              "payload": "Thêm",
              "type": "oa.query.show"
           },
           {
              "title": "Xóa món",
              "payload": "Xóa",
              "type": "oa.query.show"
           },
           {
              "title": "Hủy",
              "payload": "Hủy",
              "type": "oa.query.show"
           }
          ],
        }
      }
    }
  }
  response = requests.post(url= API_URL +"oa/message?access_token=" + ACCESS_TOKEN,
    json=message_info)
  print("\nReply user by select: ", response.json())
  return response.json()

def reply_user_select_yes_no(user_id, msg: str, sub_msg: str, img_url: str):
  message_info = {
    'recipient': {
      'user_id': user_id
    },
    'message': {
      'attachment': {
        'type': "template",
        'payload': {
          "template_type": "list",
          "elements": [{
            "title": msg,
            "subtitle": sub_msg,
            "image_url": img_url
          }],
          "buttons": [
           {
              "title": "Có",
              "payload": "Có",
              "type": "oa.query.show"
           },
           {
              "title": "Không",
              "payload": "Không",
              "type": "oa.query.show"
           }
          ],
        }
      }
    }
  }
  response = requests.post(url= API_URL +"oa/message?access_token=" + ACCESS_TOKEN,
    json=message_info)
  print("\nReply user by select yes no: ", response.json())
  return response.json()

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

def get_new_products(limit: int):
  user_id, msg, event = receive_user_text()

  all_products = get_products(False)
  new_products = utils_zalo.sort_new_products(all_products, limit)
  result = "Món mới cập nhật:\n"
  index = 1
  for p in new_products:
    result += utils_zalo.print_product(index = index, products = p)
    index += 1

  reply_user_text(user_id, result)
  return "Mời bạn chọn món!"

def get_best_products(limit: int):
  user_id, msg, event = receive_user_text()

  all_products = get_products(False)
  best_products = utils_zalo.sort_quan_product(all_products, limit)
  result = "Món bán chạy:\n"
  index = 1
  for p in best_products:
    result += utils_zalo.print_product(index = index, products = p)
    index += 1

  reply_user_text(user_id, result)
  return "Mời bạn chọn món!"

def get_sale_products(isIntent: bool = False):
  user_id, msg, event = receive_user_text()

  all_products = get_products(False)
  sale_products = utils_zalo.get_sale_products(all_products)
  result = "Món được giảm giá:\n"
  index = 1
  for p in sale_products:
    result += utils_zalo.print_product(index = index, products = p, sale = p['sale'])
    index += 1

  if isIntent:
    return result + "\nMời bạn chọn món!"

  reply_user_text(user_id, result)
  return "Mời bạn chọn món!"
