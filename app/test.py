#!/usr/bin/env python
# -*- coding: utf-8 -*-
from owlready2 import *
onto = get_ontology("../../Drink.owl")
onto.load()
import time
from datetime import datetime
from dialog.dialog_utils import *

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
    entities = merge_entity_by_type(entities, entity_type = "TYPE", delimiter = " ")
    entities = merge_entity_by_type(entities, entity_type = "LOCATION", delimiter = " - ")

    return entities
def merge_entity_by_type(entities, entity_type: str, delimiter: str):
    # Maybe replace "_" to  " "
    index = 0
    for entity in entities:
      if (entity["type"] == entity_type):
        merge = []
        merge.append(entity['text'].replace("_", " "))
        if (index < len(entities) - 1):
          while (entities[index + 1]['type'] == entity_type):
            merge.append(entities[index + 1]['text'].replace("_", " "))
            entities.remove(entities[index + 1])
          entity["text"] = delimiter.join(merge)
      index += 1
    return entities

if __name__ == '__main__':

#Test dialog and convert

    entities = [
    {'id': 'T1', 'type': 'QUANTITY', 'start': 4, 'end': 10, 'text': '1'},
    {'id': 'T2', 'type': 'TYPE', 'start': 11, 'end': 18, 'text': 'trà sữa'},
    {'id': 'T3', 'type': 'TYPE', 'start': 19, 'end': 25, 'text': 'bạc hà'},
    {'id': 'T4', 'type': 'TOPPING', 'start': 26, 'end': 39, 'text': 'trân_châu đen'},
    {'id': 'T5', 'type': 'SIZE', 'start': 45, 'end': 46, 'text': 'l'},
    {'id': 'T6', 'type': 'ADJUSTSUGAR', 'start': 47, 'end': 59, 'text': '50 đường'},
    {'id': 'T7', 'type': 'ADJUSTICE', 'start': 60, 'end': 69, 'text': '50 đá'},
    {'id': 'T8', 'type': 'QUANTITY', 'start': 70, 'end': 76, 'text': '2'},
    {'id': 'T9', 'type': 'TYPE', 'start': 77, 'end': 92, 'text': 'trà sữa dâu tây'},
    {'id': 'T10', 'type': 'TOPPING', 'start': 93, 'end': 106, 'text': 'trân_châu sợi'},
    {'id': 'T12', 'type': 'LOCATION', 'start': 117, 'end': 123, 'text': '143'},
    {'id': 'T13', 'type': 'LOCATION', 'start': 124, 'end': 139, 'text': 'phạm_ngọc_thạch'},
    {'id': 'T14', 'type': 'PHONE', 'start': 148, 'end': 153, 'text': '0385895817'}]

    intents = ["order", "product", "location"]

    user_msg = "Yololo"

    dialog = create_dialog("user_id")
    print("New dialog: ", dialog)

    print("\n", intents, entities)
    intent = convert_intents(intents)
    entities = convert_entities(entities)
    print("\nUpdated intent, entities: ", intent, entities)
    update_snips(dialog = dialog, msg = user_msg, intent = intent, entities = entities)
    print("\nUpdated diialog: ", dialog)

    intent = "order_product_ing"
    print(intent[:len(intent) - 4])
    print(intent.replace("_ing", ""))


#District convert
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
