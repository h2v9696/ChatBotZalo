import app.api.zalo_api as zaloAPI
import app.utils.utils_zalo as utils_zalo
from app.dialog.dialog_utils import *
from app.dialog.const import START_STATE, ORDERED_STATE, ORDERING_STATE

class HandleDetail:
  def __init__(self):
    pass

  def order_product(self, dialog: dict, state: str):
    """
    user ask to order somethings
    :param conversation: dict
    :param state: str
    :return dialog with new response:
    """
    userProfile = zaloAPI.get_user_profile(dialog['user_id'])
    # Check missing entities
    order = {
      'customer':
      {
          'name': userProfile['data']['displayName'],
          'phone': '',
          'user_id': userProfile['data']['userId'],
          'address': '',
          'district': 1,
          'city': 1
      },
      'order_items': [],
      'extra_note': "Ghi chú từ khách hàng: "
    }
    index = 0
    # Maybe use pop to clear entities?
    entities = dialog['snips']['entities'][0]

    for e in entities:
      if (entities.index(e) == index):
        e['value'] = e['value'].replace("_", " ")
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
          if (index != 0):
            if (entities[index - 1]['label'] == 'QUANTITY'):
              item['quantity'] = int(entities[index - 1]['value'])
          # Get type to product name
          item['product_name'] = e['value']
          # Get 'SIZE' 'TOPPING' 'ADJUSTICE' 'ADJUSTSUGAR' behind TYPE
          # to Order TOPPING, change product size or add condition to product in extra_note
          extra_note.append(item['product_name'])
          if (index < len(entities) - 1):
            while (entities[index + 1]['label'] == 'SIZE'
                      or entities[index + 1]['label'] == 'TOPPING'
                      or entities[index + 1]['label'] == 'ADJUSTICE'
                      or entities[index + 1]['label'] == 'ADJUSTSUGAR'):
              entities[index + 1]['value'] = entities[index + 1]['value'].replace("_", " ")
              if entities[index + 1]['label'] == 'SIZE':
                item['variation']['id'] = utils_zalo.convert_id_size(id_or_size = entities[index + 1]['value'])
              if entities[index + 1]['label'] == 'TOPPING':
                extra_note.append("Topping: " + entities[index + 1]['value'])
                # Order Topping
                topping_item = {
                  'product_id': '',
                  'product_name': entities[index + 1]['value'],
                  'quantity': item['quantity'],
                }
                order['order_items'].append(topping_item)
              if entities[index + 1]['label'] == 'ADJUSTICE':
                extra_note.append("Lượng đá: " + entities[index + 1]['value'])
              if entities[index + 1]['label'] == 'ADJUSTSUGAR':
                extra_note.append("Lượng đường: " + entities[index + 1]['value'])
              e = entities[index + 1]
              index += 1
          # Append to order
          if (len(extra_note) != 0):
            order['extra_note'] += ', '.join(extra_note) + '; '
          order['order_items'].append(item)

        if (e['label'] == 'LOCATION'):
          district = utils_zalo.get_district_id(address = e['value'].replace('_', ' '))
          # If cant get district id then let it default is 1 else change default district and remove district from location
          if (district == 0):
            order['customer']['address'] = e['value']
          else:
            order['customer']['address'] = e['value'].replace(utils_zalo.get_district_from_id(district), '')
            order['customer']['address'] = order['customer']['address'][:-1]
            order['customer']['district'] = district

        if (e['label'] == 'PHONE'):
          order['customer']['phone'] = e['value']

        index += 1

    # Confirm order
    all_products = zaloAPI.get_products(False)
    product = None
    order_confirm = "Bạn xác nhận lại giúp mình thông tin đơn hàng nhé\nĐơn hàng:\n"
    order_confirm += "Người đặt hàng: " + order['customer']['name'] + "\nSố điện thoại: " + order['customer']['phone']
    order_confirm += "\nĐịa chỉ: " + order['customer']['address'].title() + ", " + utils_zalo.get_district_from_id(id = order['customer']['district']).title() + ", " + "Hà Nội\n"
    order_confirm += "Sản phẩm:\n"
    p_index = 1
    total_price = 0
    # Get product id to complete order
    for item in order['order_items']:
      product = utils_zalo.get_product(all_products, product_name = item['product_name'])
      order_confirm += str(p_index) + ": " + product['name'] + " Size: "
      order_confirm += (utils_zalo.convert_id_size(id_or_size = item['variation']['id']).upper() if not (item['variation']['id'] == '') else "M")
      order_confirm += " - SLL: " + str(item["quantity"]) + " Giá: "
      # print(product)
      if 'variations' in product:
        for v in product['variations']:
          if item['variation']['id'] == '' and utils_zalo.convert_id_size(id_or_size = v['attributes'][0]) == 'm':
            item['variation']['id'] = v['id']
            total_price += int(v['price']) * item["quantity"]
            order_confirm += str(int(v['price']) * item["quantity"]) + " đ\n"
            break
          if v['attributes'][0] == item['variation']['id']:
            item['variation']['id'] = v['id']
            total_price += int(v['price']) * item["quantity"]
            order_confirm += str(int(v['price']) * item["quantity"]) + " đ\n"
      else:
        if "variation" in item:
          del item["variation"]
        total_price += int(product['price']) * item["quantity"]
        order_confirm += str(int(product['price']) * item["quantity"]) + " đ\n"
      p_index += 1
      item['product_id'] = product["id"]
      item['product_name'] = product["name"]
    # print(order)
    order_confirm += "Tổng giá: " + str(total_price) + " đ\nGhi chú: " + order['extra_note']
    # Fix later
    response = {
      "reply_type": "reply_select",
      "reply": "Xác nhận đặt hàng",
      "sub_reply": order_confirm,
      "image_url":  product['photo_links'][0]
    }
    dialog = set_response(dialog = dialog, response = response)
    # confirm = zaloAPI.reply_user_select_yes_no(userProfile['data']['userId'], msg = "Xác nhận đặt hàng", sub_msg = order_confirm, img_url = product['photo_links'][0])
    dialog['variable'] = order
    dialog = set_state(dialog = dialog, state = state.replace("_ing", "_confirm"))
    return dialog

  def order_product_confirm(self, dialog: dict, state: str):
    if (dialog["snips"]["sentence"] == "Xác nhận"):
      # Confirm
      response = zaloAPI.create_order(dialog['variable'])
      if (response['error'] != 0):
        result = "Xin lỗi bạn quá trình order đã gặp vấn đề: " + response['message'] + "\nXin bạn thử lại sau."
      else:
        result = "Mình đã tạo order rồi nhé, mời bạn kiểm tra."
    else:
      result = "Mình đã hủy thông tin đặt hàng."

    # End order change state to begin
    dialog = set_state(dialog = dialog, state = START_STATE)
    # Clear entities variable
    response = {
      "reply_type": "reply_text",
      "reply": result
    }
    dialog = set_response(dialog = dialog, response = response)
    return dialog
