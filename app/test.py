#!/usr/bin/env python
# -*- coding: utf-8 -*-
from owlready2 import *
onto = get_ontology("../../Drink.owl")
onto.load()
import time
from datetime import datetime
import json
from dialog.const import START_STATE, ORDER_INTENT, ORDERING_STATE
import pprint
#Test dialog and convert method
def convert_intents(intents):
  """
  Convert 3 intents into 1 intent
  """
  question_type = intents[0]
  domain = intents[1]
  question_attr = intents[2]
  if (question_type == "order" and domain == "product"):
    return "order_product"
  return None
def convert_entities(entities):
  """
  Convert entities n "TYPE" > 1 "TYPE", n "LOCATION" > 1 "LOCATION" ...
  """
  for e in entities:
    e['text'] = e['text'].replace("_", " ")
  entities = merge_entity_by_type(entities, entity_type = "TYPE", delimiter = " ")
  entities = merge_entity_by_type(entities, entity_type = "LOCATION", delimiter = " - ")

  return entities

def get_product(all_products, product_name: str, full_word: bool = False):
  # print(all_products)
  product_name = product_name.replace("_", " ")
  if (len(all_products) != 0):
    for p in all_products:
      if full_word:
        if product_name == p.lower():
          return p
      else:
        if product_name in p.lower():
          return p

  return None

def merge_entity_by_type(entities, entity_type: str, delimiter: str):
  all_products = [
    "trà sữa chocolate",
    "trà sữa matcha",
    "trà sữa dâu tây",
    "trà sữa bạc hà",
  ]
  # index = 0
  merge = ""

  for index, entity in enumerate(entities):
    print(index, entity, '\n')
    if (entity["type"] == entity_type):
      merge = entity['text']
      # merge.append(entity['text'])
      if (index < len(entities) - 1):
        i = index + 1
        while (entities[i]['type'] == entity_type):
          # merge.append(entities[index + 1]['text'])
          if (entity_type == "TYPE"):
            if (get_product(all_products, merge + delimiter + entities[i]['text'], full_word = True)):
              merge += delimiter + entities[i]['text']
              # entities.remove(entities[i])
              entities.pop(i)
            else:
              i += 1
          else:
            merge += delimiter + entities[i]['text']
            entities.pop(i)

          if (i > len(entities) - 1):
              break
        # entity["text"] = delimiter.join(merge)
      entity["text"] = merge
  return entities
def create_dialog(user_id):
    """
    Create dialog
    :param user_id: id
    :return:
    """
    if user_id:
      dialog = {
        "user_id": user_id
      }
    dialog.update({
        "state": START_STATE,
        "snips": {
          "sentence": "",
          "intent": "",
          "entities": []
        },
        "responses": {},
        "variable": {}
    })

    return dialog

# def set_response(dialog: dict, response: str):
#   dialog["responses"] = response
#   return dialog
# def get_state(dialog: dict):
#   return dialog['state']
# def set_state(dialog: dict, state: str):
#   dialog['state'] = state
#   return dialog
# def update_snips(dialog: dict, msg: str, intent: list, entities: list):
#   dialog["snips"]["sentence"] = msg
#   dialog["snips"]["intent"] = intent
#   current_state = get_state(dialog)
#   if (current_state == START_STATE):
#     add_entities(dialog = dialog, entities = entities)
#   else:
#     update_entities(dialog = dialog, entities = entities)
#   # for entity in entities:
#   #   new_entity = {
#   #     "label": entity['type'],
#   #     "value": entity['text']
#   #   }
#   #   dialog["snips"]['entities'].append(new_entity)

#   return dialog
# def add_entities(dialog: dict, entities: list):
#   new_entities = []
#   for entity in entities:
#     new_entity = {
#       "label": entity['type'],
#       "value": entity['text']
#     }
#     # Entities cua 1 intent moi
#     new_entities.append(new_entity)
#   dialog['snips']['entities'].insert(0, new_entities)
#   return dialog

# def update_entities(dialog: dict, entities: list):
#   print("??")
#   old_entities = dialog['snips']['entities'][0]
#   new_entities = []
#   index = 0
#   for entity in entities:
#     new_entity = {
#       "label": entity['type'],
#       "value": entity['text']
#     }
#     # Update or add new at first entites
#     is_new = True
#     for old_entity in old_entities:
#       if old_entity["label"] == new_entity["label"]:
#         old_entity["value"] = new_entitiy["value"]
#         is_new = False
#         # if old_entity["label"] == "TYPE":
#         break
#     if is_new:
#       old_entities.append(new_entity)
#       # Temporarity append later: 'SIZE' 'TOPPING' 'ADJUSTICE' 'ADJUSTSUGAR' need to be behind 'TYPE'
#   return dialog
# def check_missing_entity(dialog: dict, intent: str):
#   entities = dialog['snips']['entities'][0]
#   missing_entities = []
#   # Check missing entity in order section
#   if (intent == ORDER_INTENT or intent == ORDERING_STATE):
#     # Full entity TYPE PHONE LOCATION
#     countPhone = 0
#     countLoc = 0
#     for entity in entities:
#       if entity['label'] == 'PHONE':
#         countPhone += 1
#       if entity['label'] == 'LOCATION':
#         countLoc += 1
#     if countPhone == 0:
#       missing_entities.append('PHONE')
#     if countLoc == 0:
#       missing_entities.append('LOCATION')

#   return missing_entities
# def __merge_product(order: dict):
#   items = order['order_items']
#   # Merge same product to 1 and add quantity
#   for index, item in enumerate(items):
#     for index_2, item_2 in enumerate(items):
#       if (index_2 <= index):
#         continue
#       # print("\nItem1 - Item2: ", index, json.dumps(item, indent=2, ensure_ascii = False), index_2, json.dumps(item_2, indent=2, ensure_ascii = False), "\n")

#       # if item_2['product_id'] == item['product_id']:
#       if __except_key(d = item_2, keys = ['quantity']) == __except_key(d = item, keys = ['quantity']):
#         item['quantity'] += item_2['quantity']
#         # print("\nRemove Item2: ", index_2, json.dumps(item_2, indent=2, ensure_ascii = False), "\n")
#         items.remove(item_2)
#   return order

def __except_key(d: dict, keys: list):
  return {k: d[k] for k in set(list(d.keys())) - set(keys)}

def __swap_product(new_entities, old_entities):
  return old_entities

if __name__ == '__main__':
# Test swap product
  entities = [
    {
      "label": "TYPE",
      "value": "trà sữa chocolate",
      "parent": ""
    }
  ]

  old_entities = [
    {
      "label": "QUANTITY",
      "value": "1",
      "parent": "trà sữa chocolate"
    },
    {
      "label": "TYPE",
      "value": "trà sữa chocolate",
      "parent": ""
    },
    {
      "label": "SIZE",
      "value": "l",
      "parent": "trà sữa chocolate"
    },
    {
      "label": "TOPPING",
      "value": "thạch pudding",
      "parent": "trà sữa chocolate"
    },
    {
      "label": "LOCATION",
      "value": "đại cồ việt",
      "parent": ""
    },
    {
      "label": "PHONE",
      "value": "01684894818",
      "parent": ""
    }
  ]
# Delete unneccessary entities
  # index = 0
  # while (index < len(old_entities)):
  #     entity = old_entities[index]
  #     print (index, entity, '\n')
  #     if not (entity['label'] == 'LOCATION' or entity['label'] == 'PHONE'):
  #       print(old_entities.pop(index),'\n')
  #     else:
  #       index += 1

  print("\nDecrease section\n")
  isProductExist = False

  o_index = 0
  while (o_index < len(old_entities)):
    o_entity = old_entities[o_index]
    print (o_index, o_entity, '\n')
    if (o_entity['label'] == "TYPE"):
      if o_entity in entities:
        isProductExist = True
        print(old_entities.pop(o_index), '\n')
        o_index -= 1
        i = 0
        while (i < len(old_entities)):
          e = old_entities[i]
          if (e["parent"] == o_entity['value']):
            print(old_entities.pop(i), '\n')
            i -=1
          i += 1
    o_index += 1

  print("\nUpdated entities: ", json.dumps(old_entities, indent=2, ensure_ascii = False))


# Test merge product
  # order = {
  #   "customer": {
  #     "name": "Hoàng Quốc Việt",
  #     "phone": "0683727172",
  #     "user_id": 4082553424673949951,
  #     "address": "15 chùa bộc",
  #     "district": 1,
  #     "city": 1
  #   },
  #   "order_items": [
  #     {
  #       "product_id": "f29281d686936fcd3682",
  #       "product_name": "Thạch cà phê",
  #       "quantity": 1
  #     },
  #     {
  #       "product_id": "38c18d868ac3639d3ad2",
  #       "product_name": "Hồng trà đào",
  #       "quantity": 1,
  #       "variation": {
  #         "id": "a451eb7bf33e1a60432f"
  #       }
  #     },
  #     {
  #       "product_id": "38c18d868ac3639d3ad2",
  #       "product_name": "Hồng trà đào",
  #       "quantity": 2,
  #       "variation": {
  #         "id": "a451eb7bf33e1a60432d"
  #       }
  #     },
  #     {
  #       "product_id": "f29281d686936fcd3682",
  #       "product_name": "Thạch cà phê",
  #       "quantity": 2
  #     },
  #     {
  #       "product_id": "38c18d868ac3639d3ad2",
  #       "product_name": "Hồng trà đào",
  #       "quantity": 1,
  #       "variation": {
  #         "id": "a451eb7bf33e1a60432d"
  #       }
  #     }
  #   ],
  #   "extra_note": "hồng trà đào, Topping: thạch cà phê; "
  # }

  # print("\nOutput: ", json.dumps(__merge_product(order), indent=2, ensure_ascii = False))
# Test dialog and convert

  # entities = [
  # {'id': 'T1', 'type': 'QUANTITY', 'start': 4, 'end': 10, 'text': '1'},
  # {'id': 'T2', 'type': 'TYPE', 'start': 11, 'end': 18, 'text': 'trà sữa'},
  # {'id': 'T3', 'type': 'TYPE', 'start': 19, 'end': 25, 'text': 'bạc hà'},
  # {'id': 'T4', 'type': 'TOPPING', 'start': 26, 'end': 39, 'text': 'trân_châu đen'},
  # {'id': 'T5', 'type': 'SIZE', 'start': 45, 'end': 46, 'text': 'l'},
  # {'id': 'T6', 'type': 'ADJUSTSUGAR', 'start': 47, 'end': 59, 'text': '50 đường'},
  # {'id': 'T7', 'type': 'ADJUSTICE', 'start': 60, 'end': 69, 'text': '50 đá'},
  # {'id': 'T8', 'type': 'QUANTITY', 'start': 70, 'end': 76, 'text': '2'},
  # {'id': 'T4', 'type': 'TYPE', 'start': 11, 'end': 18, 'text': 'trà sữa'},
  # {'id': 'T9', 'type': 'TYPE', 'start': 77, 'end': 92, 'text': 'dâu tây'},
  # {'id': 'T10', 'type': 'TOPPING', 'start': 93, 'end': 106, 'text': 'trân_châu sợi'},
  # {'id': 'T12', 'type': 'LOCATION', 'start': 117, 'end': 123, 'text': '143'},
  # {'id': 'T13', 'type': 'LOCATION', 'start': 124, 'end': 139, 'text': 'phạm_ngọc_thạch'}
  # ]
  # intents = ["order", "product", "location"]
  # intent = convert_intents(intents)
  # entities = convert_entities(entities)
  # print("\nUpdated intent, entities: ", intent, json.dumps(entities, indent=2, ensure_ascii = False))
  # user_msg = "Yololo"
  # _d = {'a': {'1': [],'2': []},'b': {'1': [],'2': [],}}
  # pprint.pprint (_d)
  # dialog = create_dialog("user_id")
  # print("New dialog: ", json.dumps(dialog, indent = 2, ensure_ascii = False))

  # print("\n", intents, "\n", json.dumps(entities, indent=2, ensure_ascii = False))

  # update_snips(dialog = dialog, msg = user_msg, intent = intent, entities = entities)
  # print("\nUpdated dialog: ", json.dumps(dialog, indent=2, ensure_ascii = False))

  # intent = "order_product_ing"
  # print(intent[:len(intent) - 4])
  # print(intent.replace("_ing", ""))

# Test District convert
    # DISTRICTS = {
    #   'ba đình': 1, 'hoàn kiếm': 2, 'tây hồ': 3, 'long biên': 4, 'cầu giấy': 5, 'đống đa': 6, 'hai bà trưng': 7,
    #   'hoàng mai': 8, 'thanh xuân': 9, 'sóc sơn': 16, 'đông anh': 17, 'gia lâm': 18, 'nam từ liêm': 19, 'thanh trì': 20,
    #   'bắc từ liêm': 21, 'mê linh': 250, 'hà đông': 268, 'sơn tây': 269, 'ba vì': 271, 'phúc thọ': 272, 'đan phượng': 273,
    #   'hoài đức': 274, 'quốc oai': 275, 'thạch thất': 276, 'chương mỹ': 277, 'thanh oai': 278, 'thường tín': 279,
    #   'phú xuyên': 280, 'ứng hòa': 281, 'mỹ đức': 282
    # }
    # address = "huyện đông anh"
    # for d in DISTRICTS:
    #   if d in address.lower():
    #     print(DISTRICTS[d])
    #     break

# Test convert time
    # unix_timestamp  = int("1486731896687")
    # utc_time = time.ctime(1554803360945/1000)
    # local_time = time.localtime(unix_timestamp)
    # print(time.strftime("%Y-%m-%d %h:%M:%S", local_time))

    # readable = datetime.fromtimestamp(1554803360945/1000)
    # print(readable.strftime('%H:%M %d/%m/%Y'))

    # print(list(onto.classes()))
    # print(onto.search(iri = "*trà*"))
    # print(onto["trà_sữa"].name)
    # print(onto["trà_oolong"].is_a)
    # if (read.isTest):
    #     for line in read.read_file('test'):
    #         print line[0] + ' ' + line[1] + ' ' + unicode(line[2], 'utf-8')
    # else:
    #     for line in read.read_file('../GR/Data/domain/product.txt'):
    #         print line[0] + ' ' + unicode(line[1], 'utf-8')

# Test get entities
    # order = {
    #   'customer':
    #   {
    #       'name': "userProfile['data']['displayName']",
    #       'phone': '',
    #       'user_id': "userProfile['data']['userId']",
    #       'address': '',
    #       'district': 2,
    #       'city': 1
    #   },
    #   'order_items': [],
    #   'extra_note': "Ghi chú từ khách hàng"
    # }
    # address = []
    # extra_note = []
    # index = 0
    # for e in entities:
    #   if (entities.index(e) == index):
    #     print(e, index)
    #     if (e['type'] == 'TYPE'):
    #       item = {
    #         'product_id': '',
    #         'product_name': '',
    #         'quantity': 1,
    #       }
    #       # Get product 'QUANTITY' if dont have 'QUANTITY' before that then dafault = 1
    #       if (index != 0):
    #         if (entities[index - 1]['type'] == 'QUANTITY'):

    #           item['quantity'] = int(entities[index - 1]['text'])
    #       # Get all 'TYPE' stand together
    #       product = []
    #       product.append(e['text'])
    #       if (index < len(entities) - 1):
    #         while (entities[index + 1]['type'] == 'TYPE'):
    #           product.append(entities[index + 1]['text'])
    #           e = entities[index + 1]
    #           index += 1
    #         item['product_name'] = ' '.join(product)
    #       # Get 'SIZE' 'TOPPING' 'ADJUSTICE' 'ADJUSTSUGAR' behind TYPE
    #       size = ""
    #       extra_note.append(item['product_name'])
    #       if (index < len(entities) - 1):
    #         while (entities[index + 1]['type'] == 'SIZE'
    #                   or entities[index + 1]['type'] == 'TOPPING'
    #                   or entities[index + 1]['type'] == 'ADJUSTICE'
    #                   or entities[index + 1]['type'] == 'ADJUSTSUGAR'):
    #           if entities[index + 1]['type'] == 'SIZE':
    #             size = entities[index + 1]['text']
    #           if entities[index + 1]['type'] == 'TOPPING':
    #             extra_note.append("Topping: " + entities[index + 1]['text'].replace("_", " "))
    #             topping_item = {
    #               'product_id': '',
    #               'product_name': entities[index + 1]['text'].replace("_", " "),
    #               'quantity': item['quantity'],
    #             }
    #             order['order_items'].append(topping_item)
    #             # Order Topping
    #           if entities[index + 1]['type'] == 'ADJUSTICE':
    #             extra_note.append("Lượng đá: " + entities[index + 1]['text'])
    #           if entities[index + 1]['type'] == 'ADJUSTSUGAR':
    #             extra_note.append("Lượng đường: " + entities[index + 1]['text'])
    #           e = entities[index + 1]
    #           index += 1
    #       # Append to order
    #       if (len(extra_note) != 0):
    #           order['extra_note'] = ', '.join(extra_note)
    #       order['extra_note'] = ', '.join(extra_note) + '; '
    #       order['order_items'].append(item)

    #     if (e['type'] == 'LOCATION'):
    #       address.append(e['text'].replace('_', ' '))

    #     if (e['type'] == 'PHONE'):
    #       order['customer']['phone'] = e['text']

    #     index += 1

    # order['customer']['address'] = ' - '.join(address)
    # print(order)
