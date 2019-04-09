#!/usr/bin/env python
# -*- coding: utf-8 -*-
from owlready2 import *
onto = get_ontology("../../Drink.owl")
onto.load()
import time

# Test convert time
# unix_timestamp  = int("1486731896687")
# utc_time = time.ctime(1554803360945/1000)
# local_time = time.localtime(unix_timestamp)
# print(time.strftime("%Y-%m-%d %H:%M:%S", local_time))

# from datetime import datetime
# readable = datetime.fromtimestamp(1554803360945/1000)
# print(readable.strftime('%H:%M %d/%m/%Y'))

if __name__ == '__main__':
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

    #Test get entities
    # entities = [
    # {'id': 'T1', 'type': 'QUANTITY', 'start': 4, 'end': 10, 'text': '1'},
    # {'id': 'T2', 'type': 'TYPE', 'start': 11, 'end': 18, 'text': 'trà sữa'},
    # {'id': 'T3', 'type': 'TYPE', 'start': 19, 'end': 25, 'text': 'bạc hà'},
    # {'id': 'T4', 'type': 'TOPPING', 'start': 26, 'end': 39, 'text': 'trân_châu đen'},
    # {'id': 'T5', 'type': 'SIZE', 'start': 45, 'end': 46, 'text': 'l'},
    # {'id': 'T6', 'type': 'ADJUSTSUGAR', 'start': 47, 'end': 59, 'text': '50 đường'},
    # {'id': 'T7', 'type': 'ADJUSTICE', 'start': 60, 'end': 69, 'text': '50 đá'},
    # {'id': 'T8', 'type': 'QUANTITY', 'start': 70, 'end': 76, 'text': '2'},
    # {'id': 'T9', 'type': 'TYPE', 'start': 77, 'end': 92, 'text': 'trà sữa dâu tây'},
    # {'id': 'T10', 'type': 'TOPPING', 'start': 93, 'end': 106, 'text': 'trân_châu sợi'},
    # {'id': 'T12', 'type': 'LOCATION', 'start': 117, 'end': 123, 'text': '143'},
    # {'id': 'T13', 'type': 'LOCATION', 'start': 124, 'end': 139, 'text': 'phạm_ngọc_thạch'},
    # {'id': 'T14', 'type': 'PHONE', 'start': 148, 'end': 153, 'text': '0385895817'}]
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
