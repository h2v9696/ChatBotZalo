DISTRICTS = {
  'ba đình': 1, 'hoàn kiếm': 2, 'tây hồ': 3, 'long biên': 4, 'cầu giấy': 5, 'đống đa': 6, 'hai bà trưng': 7,
  'hoàng mai': 8, 'thanh xuân': 9, 'sóc sơn': 16, 'đông anh': 17, 'gia lâm': 18, 'nam từ liêm': 19, 'thanh trì': 20,
  'bắc từ liêm': 21, 'mê linh': 250, 'hà đông': 268, 'sơn tây': 269, 'ba vì': 271, 'phúc thọ': 272, 'đan phượng': 273,
  'hoài đức': 274, 'quốc oai': 275, 'thạch thất': 276, 'chương mỹ': 277, 'thanh oai': 278, 'thường tín': 279,
  'phú xuyên': 280, 'ứng hòa': 281, 'mỹ đức': 282
}

# Utils
# Retrieve product from zalo by product name
def get_product(all_products, product_name: str):
  # print(all_products)
  product_name = product_name.replace("_", " ")
  if (len(all_products) != 0):
    for p in all_products:
      if product_name in p['name'].lower():
        return p
  return None

# Convert id to size and reserve
def convert_id_size(id_or_size: str):
  id_or_size = id_or_size.lower()
  if (id_or_size == '1803545c6c198547dc08'):
    return 'm'
  elif (id_or_size == 'fcb7b1e889ad60f339bc'):
    return 'l'
  elif (id_or_size == 'm'):
    return '1803545c6c198547dc08'
  elif (id_or_size == 'l'):
    return 'fcb7b1e889ad60f339bc'

def get_category_from_id(categories, id: str):
  for c in categories:
    if (id == c['id']):
      return c['name']

# print product from list of products (use in menu)
def print_product(index: int, products: list):
  if 'variations' not in products:
    return "{:<2}\t{:<} - {:<}".format(str(index),products['name'],str(products['price'])) + "đ\n"
  else:
    m_price = 0
    l_price = 0
    for v in products['variations']:
      if convert_id_size(v['attributes'][0]) == 'm':
        m_price = "M: " + str(int(v['price'])) + "đ"
      if convert_id_size(v['attributes'][0]) == 'l':
        l_price = "L: " + str(int(v['price'])) + "đ\n"
    return "{:<2}\t{:<} - {:<} - {:<}".format(str(index),products['name'], m_price, l_price)

def get_district_id(address: str):
  for d in DISTRICTS:
    if d in address.lower():
      return DISTRICTS[d]
  return 0
