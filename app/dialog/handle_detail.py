import app.api.zalo_api as zaloAPI
import app.utils.utils_zalo as utils_zalo
import re
from app.dialog.dialog_utils import *
from app.dialog.const import START_STATE, ORDERED_STATE, ORDERING_STATE, \
                                                ORDERING_STATE_ADD, ORDERING_STATE_SWAP, ORDERING_STATE_DEC, \
                                                ORDERING_STATE_NOTE, ASK_PRICE_INTENT, ASKING_PRICE_STATE, \
                                                ASK_TIME_INTENT, ASK_LOC_INTENT, YESNO_SHIP_INTENT, PROMOTION_INTENT, \
                                                ASK_PRODUCT_SIZE_INTENT, ASK_PHONE_INTENT
from app.utils.sentences import CONFIRM, REFUSE, CHANGE, ADD, DEC, SWAP, ASK_FOR_MORE_INFO, ASK_FOR_ONE_INFO, \
  CREATED_ORDER, SORRY_FOR_ERROR_CREATE_ORDER, SORRY_FOR_ERROR, \
  ASK_FOR_CHANGE_INFO, ASK_FOR_ADD_INFO, WAIT_FIX_ORDER, CANCELED_ORDER, \
  ASK_CAUSE_WRONG_PHONE, ASK_CAUSE_NO_PRODUCT, ASK_FOR_CONFIRM, ASK_FOR_DEL_INFO, \
  PRODUCT_NOT_IN_ORDER, ASK_FOR_MORE_NOTE, GET_REFUSE, ADD_MORE_NOTE_RESPONSE, \
  SORRY_CAUSE_PRODUCT_OUT_STOCK, BAD, NOT_BAD, SORRY_FOR_BAD_REPORT, CALL_BOSS, THANKS, YES, \
  WAIT_PROCESS_ORDER, ANSWER_SHOP_TIME, ANSWER_SHOP_LOC, ANSWER_YESNO_SHIP, OTHER, \
  ANSWER_PROMOTION, ANSWER_PRODUCT_SIZE, NO_ENTITIES, ANSWER_SHOP_PHONE
from app.utils.sentence_utils import *
import json

class HandleDetail:
  def __init__(self):
    pass
# order section
  def order_product(self, dialog: dict, state: str):
    """
    user ask to order somethings
    :param conversation: dict
    :param state: str
    :return dialog with new response:
    """
    isNewEntities = True
    entities = []

    if len(dialog['snips']['entities']) > 0:
      if (get_state(dialog) == START_STATE or len(dialog['snips']['entities']) == 1):
        entities = dialog['snips']['entities'][0]
      else:
        isNewEntities = False
        entities = dialog['snips']['entities'].pop(0)
    else:
      response = {
        "reply_type": "reply_text",
        "reply": get_random_reply(replies = NO_ENTITIES)
      }
      dialog = set_response(dialog = dialog, response = response)
      return dialog

    if not isNewEntities and len(dialog['snips']['entities']) > 0:
      old_entities = dialog['snips']['entities'][0]
# Check if changing the order
    if (len(entities) > 0):
      if get_state(dialog) == ORDERING_STATE_ADD:
        # Add more 'TYPE'
        # print("\nAdding section\n")
        if not isNewEntities:
          dialog = update_entities(dialog = dialog, entities = entities)
          entities = []
      elif get_state(dialog) == ORDERING_STATE_SWAP:
        # print("\nChanging section\n")
        isProductExist = False
        for index, entity in enumerate(entities):
          if (entity['label'] == "TYPE"):
            if self.__check_exist_product_in_order(entity['value'] , old_entities):
              last = entities.pop(index)
              dialog = update_entities(dialog = dialog, entities = entities, last_entity = last)

              isProductExist = True
              for o_index, o_entity in enumerate(old_entities):
                if (o_entity['label'] == "TYPE"):
                  self.__swap_or_insert_value_in_entities(label = "SIZE", parent = o_entity['value'], entities = entities, old_entities = old_entities)
                  self.__swap_or_insert_value_in_entities(label = "TOPPING", parent = o_entity['value'], entities = entities, old_entities = old_entities)
                  self.__swap_or_insert_value_in_entities(label = "ADJUSTICE", parent = o_entity['value'], entities = entities, old_entities = old_entities)
                  self.__swap_or_insert_value_in_entities(label = "ADJUSTSUGAR", parent = o_entity['value'], entities = entities, old_entities = old_entities)
                  self.__swap_or_insert_value_in_entities(label = "QUANTITY", parent = o_entity['value'], entities = entities, old_entities = old_entities)
          if (entity['label'] == "TOPPING"):
            if self.__check_exist_product_in_order(entity['value'] , old_entities):
              last = entities.pop(index)
              dialog = update_entities(dialog = dialog, entities = entities, last_entity = last)
              isProductExist = True
          entities = []
        if not isProductExist:
          response = {
            "reply_type": "reply_text",
            "reply": get_random_reply(replies = PRODUCT_NOT_IN_ORDER)
          }
          dialog = set_response(dialog = dialog, response = response)
          return dialog
      elif get_state(dialog) == ORDERING_STATE_DEC:
        # print("\nDecrease section\n")
        isProductExist = False

        o_index = 0
        while (o_index < len(old_entities)):
          o_entity = old_entities[o_index]
          # print (o_index, o_entity, '\n')
          if (o_entity['label'] == "TYPE"):
            if o_entity in entities:
              isProductExist = True
              old_entities.pop(o_index)
              o_index -= 1
              i = 0
              while (i < len(old_entities)):
                e = old_entities[i]
                if (e["parent"] == o_entity['value']):
                  old_entities.pop(i)
                  i -= 1
                i += 1
          o_index += 1

        entities = []
        if not isProductExist:
          response = {
            "reply_type": "reply_text",
            "reply": get_random_reply(replies = PRODUCT_NOT_IN_ORDER)
          }
          dialog = set_response(dialog = dialog, response = response)
          return dialog

    dialog = set_state(dialog = dialog, state = ORDERING_STATE)

    if (len(entities) > 0 and not isNewEntities):
      dialog = update_entities(dialog = dialog, entities = entities)

#Check if no TYPE then fail
    isNoType = True
    for entity in dialog['snips']['entities'][0]:
      if (entity['label'] == 'TYPE'):
        isNoType = False
        break
    if isNoType:
      response = {
        "reply_type": "reply_text",
        "reply": get_random_reply(replies = ASK_CAUSE_NO_PRODUCT)
      }
      dialog = set_response(dialog = dialog, response = response)
      dialog = set_state(dialog = dialog, state = START_STATE)
      return dialog
# Check missing entities
    missing_entities = check_missing_entity(dialog, state)
    if len(missing_entities) > 0:
      if check_sentence_in_group(sentence = dialog["snips"]["sentence"], group = REFUSE):
        reply = get_random_reply(replies = GET_REFUSE)
        response = {
          "reply_type": "reply_text",
          "reply": reply
        }
        dialog = set_state(dialog = dialog, state = START_STATE)
        dialog = set_response(dialog = dialog, response = response)
        return dialog
      if len(missing_entities) == 1:
        reply = get_random_reply(replies = ASK_FOR_ONE_INFO)
      else:
        reply = get_random_reply(replies = ASK_FOR_MORE_INFO)

      for missing in missing_entities:
        if missing == "PHONE":
          reply += "\n- Số điện thoại"
        if missing == "LOCATION":
          reply += "\n- Địa chỉ"
      response = {
        "reply_type": "reply_text",
        "reply": reply
      }
      dialog = set_response(dialog = dialog, response = response)
    else:
      dialog = self.__create_order_info(dialog = dialog)
    return dialog

  def order_product_confirm(self, dialog: dict, state: str):
    if check_sentence_in_group(sentence = dialog["snips"]["sentence"], group = CONFIRM):
      # Confirm
      dialog = set_state(dialog = dialog, state = ORDERING_STATE_NOTE)
      # Clear entities variable
      response = {
        "reply_type": "reply_text",
        "reply": get_random_reply(replies = ASK_FOR_MORE_NOTE)
      }
      dialog = set_response(dialog = dialog, response = response)
    elif check_sentence_in_group(sentence = dialog["snips"]["sentence"], group = CHANGE) or get_state(dialog) == ORDERING_STATE_DEC or get_state(dialog) == ORDERING_STATE_SWAP or get_state(dialog) == ORDERING_STATE_ADD:
      if check_sentence_in_group(sentence = dialog["snips"]["sentence"], group = ADD):
        dialog = set_state(dialog = dialog, state = ORDERING_STATE_ADD)
      elif check_sentence_in_group(sentence = dialog["snips"]["sentence"], group = SWAP):
        dialog = set_state(dialog = dialog, state = ORDERING_STATE_SWAP)
      elif check_sentence_in_group(sentence = dialog["snips"]["sentence"], group = DEC):
        dialog = set_state(dialog = dialog, state = ORDERING_STATE_DEC)
      else:
        dialog = set_state(dialog = dialog, state = get_state(dialog))

      if (dialog["snips"]["sentence"] == "Đổi"):
        reply = get_random_reply(replies = ASK_FOR_CHANGE_INFO)
        response = {
          "reply_type": "reply_text",
          "reply": reply
        }
        dialog = set_response(dialog = dialog, response = response)
      elif (dialog["snips"]["sentence"] == "Thêm"):
        reply = get_random_reply(replies = ASK_FOR_ADD_INFO)
        response = {
          "reply_type": "reply_text",
          "reply": reply
        }
        dialog = set_response(dialog = dialog, response = response)
      elif (dialog["snips"]["sentence"] == "Xóa"):
        reply = get_random_reply(replies = ASK_FOR_DEL_INFO)
        response = {
          "reply_type": "reply_text",
          "reply": reply
        }
        dialog = set_response(dialog = dialog, response = response)
      else:
        zaloAPI.reply_user_text(dialog['user_id'], get_random_reply(replies = WAIT_FIX_ORDER))
        dialog = self.order_product(dialog, ORDERING_STATE)
    else:
      result = get_random_reply(replies = CANCELED_ORDER)

# End order change state to begin
      dialog = set_state(dialog = dialog, state = START_STATE)
      # Clear entities variable
      response = {
        "reply_type": "reply_text",
        "reply": result
      }
      dialog = set_response(dialog = dialog, response = response)
    return dialog

  def add_more_extra_note(self, dialog: dict, state: str):
    result = ""
    if check_sentence_in_group(sentence = dialog["snips"]["sentence"], group = REFUSE):
      zaloAPI.reply_user_text(dialog['user_id'], get_random_reply(replies = GET_REFUSE))
    else:
      dialog['snips']['entities'].pop(0)
      zaloAPI.reply_user_text(dialog['user_id'], get_random_reply(replies = ADD_MORE_NOTE_RESPONSE))
      dialog['variable']['extra_note'] += " Khách ghi chú: " + dialog["snips"]["sentence"]

    response = zaloAPI.create_order(self.__merge_product(dialog['variable']))
    if (response['error'] != 0):
      if (response['message'] == 'phone of customer is invalid'):
        dialog = self.__handle_error_phone(dialog = dialog, state = ORDERING_STATE)
        return dialog
      else:
        result = get_random_reply(replies = SORRY_FOR_ERROR_CREATE_ORDER) + response['message'] + "\n"
        result += get_random_reply(replies = SORRY_FOR_ERROR)
    else:
      result = get_random_reply(replies = CREATED_ORDER)

    # End add not change state to begin
    dialog = set_state(dialog = dialog, state = START_STATE)
    # Clear entities variable
    response = {
      "reply_type": "reply_text",
      "reply": result
    }
    dialog = set_response(dialog = dialog, response = response)
    return dialog

  def handle_ask_price(self, dialog: dict, state: str):
    dialog = set_state(dialog = dialog, state = state)

    dialog = self.__create_order_info(dialog = dialog)
    # End order change state to begin
    return dialog

  def handle_ask_create_order(self, dialog: dict, state: str):
    if check_sentence_in_group(sentence = dialog["snips"]["sentence"], group = YES):
      # Confirm
      zaloAPI.reply_user_text(dialog['user_id'], get_random_reply(replies = WAIT_PROCESS_ORDER))
      dialog = self.order_product(dialog, ORDERING_STATE)
    else:
      response = {
        "reply_type": "reply_text",
        "reply": get_random_reply(replies = GET_REFUSE)
      }
      dialog = set_response(dialog = dialog, response = response)
      # End order change state to begin
      dialog = set_state(dialog = dialog, state = START_STATE)
    return dialog

# other
  def exist_product(self, dialog: dict, state: str):
    isNewEntities = True
    reply = ''
    entities = []
    if len(dialog['snips']['entities']) > 0:
      if (get_state(dialog) == START_STATE):
        entities = dialog['snips']['entities'][0]
      else:
        isNewEntities = False
        entities = dialog['snips']['entities'].pop(0)
    else:
      reply = get_random_reply(replies = NO_ENTITIES)

    all_products = zaloAPI.get_products(False)
    for e in entities:
      if (e['label'] == "TYPE" or e['label'] == "TOPPING"):
        size = ""
        for _e in entities:
          if (_e['parent'] == e['value'] and _e['label'] == "SIZE"):
            size = _e['value'].lower()
            break

        if (utils_zalo.check_if_product_exist(all_products, e['value'], size = size)):
          reply += e['value'] + " vẫn còn nha bạn\n"
        else:
          reply += "Sản phẩm " + e['value'] + " không tồn tại, hoặc đã hết hàng, xin bạn vui lòng quay lại sau nhé.\n"

    dialog = set_state(dialog = dialog, state = START_STATE)
    response = {
      "reply_type": "reply_text",
      "reply": reply[:len(reply) - 1]
    }
    dialog = set_response(dialog = dialog, response = response)
    return dialog

  def handle_sentiment(self, dialog: dict, state: str):
    reply = ""

    if check_sentence_in_group(sentence = dialog["snips"]["sentence"], group = BAD):
      reply = get_random_reply(replies = SORRY_FOR_BAD_REPORT)
    elif check_sentence_in_group(sentence = dialog["snips"]["sentence"], group = NOT_BAD):
      reply = get_random_reply(replies = THANKS)
    else:
      reply = get_random_reply(replies = CALL_BOSS)

    dialog = set_state(dialog = dialog, state = START_STATE)
    response = {
      "reply_type": "reply_text",
      "reply": reply
    }
    dialog = set_response(dialog = dialog, response = response)
    return dialog

  def handle_ask_simple_answer(self, dialog: dict, state: str):
    switcher = {
        ASK_TIME_INTENT: get_random_reply(replies = ANSWER_SHOP_TIME),
        ASK_LOC_INTENT: get_random_reply(replies = ANSWER_SHOP_LOC),
        YESNO_SHIP_INTENT: get_random_reply(replies = ANSWER_YESNO_SHIP),
        PROMOTION_INTENT: get_random_reply(replies = ANSWER_PROMOTION) + zaloAPI.get_sale_products(isIntent = True),
        ASK_PRODUCT_SIZE_INTENT: get_random_reply(replies = ANSWER_PRODUCT_SIZE),
        ASK_PHONE_INTENT: get_random_reply(replies = ANSWER_SHOP_PHONE),
    }
    print(switcher, dialog["snips"]["intent"], '\n')
    reply = switcher.get(dialog["snips"]["intent"], get_random_reply(replies = OTHER))

    dialog = set_state(dialog = dialog, state = START_STATE)
    response = {
      "reply_type": "reply_text",
      "reply": reply
    }
    dialog = set_response(dialog = dialog, response = response)
    return dialog

  def handle_yesno_product(self, dialog: dict, state: str):
    isNewEntities = True
    reply = ''
    entities = []
    if len(dialog['snips']['entities']) > 0:
      if (get_state(dialog) == START_STATE):
        entities = dialog['snips']['entities'][0]
      else:
        isNewEntities = False
        entities = dialog['snips']['entities'].pop(0)

    all_products = zaloAPI.get_products(False)
    for e in entities:
      if (e['label'] == "TYPE" or e['label'] == "TOPPING"):
        if (utils_zalo.check_if_product_exist(all_products, e['value'], size = "")):
          reply += "Shop mình có " + e['value'] + " nha bạn\n"
        else:
          reply += "Sản phẩm " + e['value'] + " không tồn tại, hoặc đã hết hàng, xin bạn vui lòng quay lại sau nhé.\n"

    if not entities:
      reply = get_random_reply(replies = NO_ENTITIES)

    dialog = set_state(dialog = dialog, state = START_STATE)
    response = {
      "reply_type": "reply_text",
      "reply": reply[:len(reply) - 1]
    }
    dialog = set_response(dialog = dialog, response = response)
    return dialog


# private section
  def __handle_error_phone(self, dialog: dict, state: str):
    dialog = set_state(dialog = dialog, state = state)
    index = 0
    while (index < len(dialog['snips']['entities'][0])):
        entity = dialog['snips']['entities'][0][index]
        if entity['label'] == 'PHONE':
          dialog['snips']['entities'][0].pop(index)
        else:
          index += 1

    response = {
      "reply_type": "reply_text",
      "reply": get_random_reply(replies = ASK_CAUSE_WRONG_PHONE)
    }
    dialog = set_response(dialog = dialog, response = response)
    return dialog

  def __handle_product_out_stock(self, dialog: dict, state: str, product: dict):
    # Delete product from entity if it out of stock
    dialog = set_state(dialog = dialog, state = state)
    # dialog['snips']['entities'][0] = (entity for entity in dialog['snips']['entities'][0] if (entity['label'] == 'LOCATION' or entity['label'] == 'PHONE'))
    index = 0
    while (index < len(dialog['snips']['entities'][0])):
        entity = dialog['snips']['entities'][0][index]
        if ((entity['parent'] != '' and  entity['parent'] in product['name'].lower()) or entity['value'] in product['name'].lower()):
          dialog['snips']['entities'][0].pop(index)
        else:
          index += 1
    response = {
      "reply_type": "reply_text",
      "reply": get_random_reply(replies = SORRY_CAUSE_PRODUCT_OUT_STOCK)
    }
    dialog = set_response(dialog = dialog, response = response)
    return dialog

  def __create_order_info(self, dialog: dict):
    userProfile = zaloAPI.get_user_profile(dialog['user_id'])

    order = {
      'customer':
      {
          'name': userProfile['data']['displayName'],
          'phone': '',
          'user_id': userProfile['data']['userId'],
          'address': '',
          'district': 0,
          'city': 1
      },
      'order_items': [],
      'extra_note': ""
    }
    index = 0
    entities = []
    # Maybe use pop to clear entities?
    # entities = dialog['snips']['entities'].pop(0)
    if len(dialog['snips']['entities']) > 0:
      entities = dialog['snips']['entities'][0]
    else:
      response = {
        "reply_type": "reply_text",
        "reply": "Xin lỗi bạn, mình đang hiểu bạn muốn báo giá nhưng không thấy bạn đề cập đến sản phẩm nào."
      }
      dialog = set_response(dialog = dialog, response = response)
      dialog = set_state(dialog = dialog, state = START_STATE)
      return dialog
    # print("\nCreate order dialog entities: ", json.dumps(entities, indent = 2, ensure_ascii = False))

    for i, e in enumerate(entities):
      if (i == index):
        if (e['label'] == 'TYPE'):
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
          # Get product 'QUANTITY' if dont have 'QUANTITY' before that then default = 1
          if (index > 0):
            i = index - 1
            while (entities[i]['parent'] == e['value']):
              if (entities[i]['label'] == 'QUANTITY'):
                item['quantity'] = int(re.findall(r'\d+', entities[i]['value'])[0])
              i -= 1
              if (i < 0):
                break
          # Get type to product name
          item['product_name'] = e['value']
          # Get 'SIZE' 'TOPPING' 'ADJUSTICE' 'ADJUSTSUGAR' behind TYPE
          # to Order TOPPING, change product size or add condition to product in extra_note
          extra_note.append(item['product_name'])
          if (index < len(entities) - 1):
            i = index + 1
            while (entities[i]['parent'] == e['value']):
              if entities[i]['label'] == 'QUANTITY' and entities[index - 1]['value'].isnumeric():
                item['quantity'] = int(entities[index - 1]['value'])
              if entities[i]['label'] == 'SIZE':
                item['variation']['id'] = utils_zalo.convert_id_size(id_or_size = entities[i]['value'])
              if entities[i]['label'] == 'TOPPING':
                extra_note.append("Topping: " + entities[i]['value'])
                # Order Topping
                topping_item = {
                  'product_id': '',
                  'product_name': entities[i]['value'],
                  'quantity': item['quantity'],
                }
                order['order_items'].append(topping_item)
              if entities[i]['label'] == 'ADJUSTICE':
                extra_note.append("Lượng đá: " + entities[i]['value'])
              if entities[i]['label'] == 'ADJUSTSUGAR':
                extra_note.append("Lượng đường: " + entities[index + 1]['value'])
              i += 1
              if (i > len(entities) - 1):
                break

          # Append to order
          if (len(extra_note) != 0):
            order['extra_note'] += ', '.join(extra_note) + '; '
          order['order_items'].append(item)

        if (e['label'] == 'LOCATION'):
          district = utils_zalo.get_district_id(address = e['value'])
          # If cant get district id then let it default is 1 else change default district and remove district from location
          if (district == 0):
            order['customer']['address'] += e['value']
          else:
            order['customer']['address'] += e['value'].replace(utils_zalo.get_district_from_id(district), '')
            order['customer']['address'] = order['customer']['address'].replace("hà nội", '')
            while order['customer']['address'][-1:] == ' ':
              order['customer']['address'] = order['customer']['address'][:-1]
            order['customer']['district'] = district

        if (e['label'] == 'PHONE'):
          order['customer']['phone'] = e['value']
          if not (len(order['customer']['phone']) == 11 or len(order['customer']['phone']) == 10):
            dialog = self.__handle_error_phone(dialog = dialog, state = ORDERING_STATE)
            return dialog
        index += 1

    # Confirm order
    product = None
    order_confirm = ""
    if (get_state(dialog = dialog) != ASKING_PRICE_STATE):
      order_confirm = "Đơn hàng:\nNgười đặt hàng: " + order['customer']['name'] + "\nSố điện thoại: " + order['customer']['phone']
      district = ", "
      if order['customer']['district'] != 0:
        district += utils_zalo.get_district_from_id(id = order['customer']['district']).title()
      else:
        order['customer']['district'] = 1
        district = ""
      order_confirm += "\nĐịa chỉ: " + order['customer']['address'].title() + district + ", " + "Hà Nội\n"
    order_confirm += "Sản phẩm:\n"
    p_index = 1
    total_price = 0
    # Get product id to complete order + fill order confirm
    if (len(order['order_items']) <= 0):
      response = {
        "reply_type": "reply_text",
        "reply": get_random_reply(replies = ASK_CAUSE_NO_PRODUCT)
      }
      dialog = set_response(dialog = dialog, response = response)
      dialog = set_state(dialog = dialog, state = START_STATE)
      return dialog

    all_products = zaloAPI.get_products(False)
    for item in order['order_items']:
      product = utils_zalo.get_product(all_products, product_name = item['product_name'])
      if product:

        order_confirm += str(p_index) + ": " + product['name']
        if 'variation' in item:
          if item['variation']['id'] == '':
            item['variation']['id'] = utils_zalo.convert_id_size(id_or_size = 'm')
          quantity = utils_zalo.get_sum_quantity_in_product(product = product, size_id = item['variation']['id'])
          # print(quantity)
          if (quantity - item["quantity"] < 0):
            zaloAPI.reply_user_text(dialog['user_id'], "Sản phẩm: " + product['name'] + " - Size: " + utils_zalo.convert_id_size(id_or_size = item['variation']['id']).upper() + (" chỉ còn " + str(quantity) + " đơn vị" if (quantity > 0) else " đã hết hàng"))
            dialog = self.__handle_product_out_stock(dialog = dialog, state = ORDERING_STATE_ADD, product = product)
            return dialog
          else:
            order_confirm += " - Size: " + (utils_zalo.convert_id_size(id_or_size = item['variation']['id']).upper() if not (item['variation']['id'] == '') else "M")
        else:
          quantity = utils_zalo.get_sum_quantity_in_product(product = product)

          if (quantity - item["quantity"] < 0):
            zaloAPI.reply_user_text(dialog['user_id'], "Sản phẩm: " + product['name'] + " đã hết hàng")
            dialog = self.__handle_product_out_stock(dialog = dialog, state = ORDERING_STATE_ADD, product = product)
            return dialog

        product = utils_zalo.check_sale_product(product)
        sale = 0
        if 'sale' in product:
          sale = product['sale']
        if sale > 0:
          zaloAPI.reply_user_text(dialog['user_id'], "Sản phẩm: " + product['name'] + " đang được giảm giá " + str(int(sale * 100)) + "%")

        order_confirm += " - SLL: " + str(item["quantity"]) + " - Giá: "
        # print(product)
        if 'variations' in product:
          for v in product['variations']:
            if v['attributes'][0] == item['variation']['id']:
              item['variation']['id'] = v['id']
              total_price += int(v['price']) * item["quantity"]
              order_confirm += str(int(v['price'] * item["quantity"] * (1 - sale))) + " đ\n"
        else:
          if "variation" in item:
            del item["variation"]
          total_price += int(product['price']) * item["quantity"]
          order_confirm += str(int(product['price'] * item["quantity"] * (1 - sale))) + " đ\n"
        p_index += 1
        item['product_id'] = product["id"]
        item['product_name'] = product["name"]

      else:
        response = {
          "reply_type": "reply_text",
          "reply": "Sản phẩm " + item['product_name'] + " không tồn tại :(( , bạn vui lòng xem lại menu giúp mình nhé."
        }
        dialog = set_response(dialog = dialog, response = response)
        dialog = set_state(dialog = dialog, state = ORDERING_STATE_SWAP)

    if product:
      if (get_state(dialog = dialog) != ASKING_PRICE_STATE):
        zaloAPI.reply_user_text(dialog['user_id'], get_random_reply(replies = ASK_FOR_CONFIRM))

      # print(order)
      order_confirm += "Tổng giá: " + str(int(total_price * (1 - sale))) + " đ"
      if (get_state(dialog = dialog) != ASKING_PRICE_STATE):
        order_confirm += "\nGhi chú: " + order['extra_note']
      # Confirm order
      if (get_state(dialog = dialog) != ASKING_PRICE_STATE):
        response = {
          "reply_type": "reply_select",
          "reply": "Xác nhận đặt hàng",
          "sub_reply": order_confirm,
          "image_url":  product['photo_links'][0]
        }
        dialog = set_state(dialog = dialog, state = ORDERED_STATE)
        dialog['variable'] = order
      else:
        zaloAPI.reply_user_text(dialog['user_id'], "Đây là tổng giá, bạn có muốn mình giúp bạn tạo đơn hàng luôn không?")

        response = {
          "reply_type": "reply_select_yes_no",
          "reply": "Báo giá",
          "sub_reply": order_confirm,
          "image_url":  product['photo_links'][0]
        }

      dialog = set_response(dialog = dialog, response = response)

    return dialog

  def __merge_product(self, order: dict):
    items = order['order_items']
    # Merge same product to 1 and add quantity
    for index, item in enumerate(items):
      for index_2, item_2 in enumerate(items):
        if (index_2 <= index):
          continue

        if self.__except_key(d = item_2, keys = ['quantity']) == self.__except_key(d = item, keys = ['quantity']):
          item['quantity'] += item_2['quantity']
          items.remove(item_2)
    return order

  # Return dict without set of keys
  def __except_key(self, d: dict, keys: list):
    return {k: d[k] for k in set(list(d.keys())) - set(keys)}

  def __check_exist_product_in_order(self, product_name: str, old_entities: list):
    for entity in old_entities:
      if (product_name in entity['value']):
        return True
    return False

  def __swap_or_insert_value_in_entities(self, label: str, parent: str, entities: dict, old_entities: dict):
    # Swap or insert in new entities and set to old entities with same label and parent
    # SIZE not swapable cuz cant catch it yet
    result = None
    for index, key in enumerate(entities):
      if key['label'] == label and key['parent'] == parent:
        result = entities.pop(index)
    if result:
      print("\nResult entities: ", json.dumps(result, indent = 2, ensure_ascii = False))
      found_index = -1
      for index, key in enumerate(old_entities):
        if key['label'] == "TYPE":
          found_index = index
        if key['label'] == label and key['parent'] == parent:
          key['value'] = result['value']
          found_index = -1
          break

      if found_index != -1:
        old_entities.insert(found_index + 1, result)
