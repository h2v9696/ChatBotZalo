DISTRICTS = {
  'ba đình': 1, 'hoàn kiếm': 2, 'tây hồ': 3, 'long biên': 4, 'cầu giấy': 5, 'đống đa': 6, 'hai bà trưng': 7,
  'hoàng mai': 8, 'thanh xuân': 9, 'sóc sơn': 16, 'đông anh': 17, 'gia lâm': 18, 'nam từ liêm': 19, 'thanh trì': 20,
  'bắc từ liêm': 21, 'mê linh': 250, 'hà đông': 268, 'sơn tây': 269, 'ba vì': 271, 'phúc thọ': 272, 'đan phượng': 273,
  'hoài đức': 274, 'quốc oai': 275, 'thạch thất': 276, 'chương mỹ': 277, 'thanh oai': 278, 'thường tín': 279,
  'phú xuyên': 280, 'ứng hòa': 281, 'mỹ đức': 282
}

SALE_PRODUCTS = {
  'trà sữa dâu tây': 0.2,
  'trà sữa đào': 0.2,
  'trà sữa chocolate': 0.2,
  'trà sữa matcha': 0.2,
  'trà sữa bạc hà': 0.2
}

# Utils
# Retrieve product from zalo by product name
def get_product(all_products, product_name: str, full_word: bool = False):
  # print(all_products)
  product_name = product_name.replace("_", " ")
  if (len(all_products) != 0):
    for p in all_products:
      if full_word:
        if product_name == p['name'].lower():
          return p
      else:
        if product_name in p['name'].lower():
          return p

  return None

def sort_new_products(all_products, limit: int):
  if limit < len(all_products):
    return sorted(all_products, key = lambda k:k['update_time'], reverse=True)[:limit]
  return sorted(all_products, key = lambda k:k['update_time'], reverse=True)

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
  return ''

def get_category_from_id(categories, id: str):
  for c in categories:
    if (id == c['id']):
      return c['name']

# print product from list of products (use in menu)
def print_product(index: int, products: list, sale: float = 0.0):
  sale_text = ""

  if 'variations' not in products:
    if sale > 0:
      sale_text = "{:<} {:<}".format("Giảm còn: ", str(int(products['price'] * (1 - sale)))) + " đ\n"
    return "{:<2}\t{:<} - {:<}".format(str(index),products['name'],str(products['price'])) + " đ\n" + sale_text
  else:
    m_price = 0
    l_price = 0
    for v in products['variations']:
      if convert_id_size(v['attributes'][0]) == 'm':
        m_price = int(v['price'])
      if convert_id_size(v['attributes'][0]) == 'l':
        l_price = int(v['price'])

    if sale > 0:
      sale_text = "{:<} {:<} - {:<}".format("Giảm còn: ", "M: " + str(int(m_price * (1 - sale))) + " đ", "L: " + str(int(l_price * (1 - sale))) + " đ\n")
    return "{:<2}\t{:<} - {:<} - {:<}".format(str(index),products['name'], "M: " + str(m_price) + " đ", "L: " + str(l_price) + " đ\n") + sale_text

def get_district_id(address: str):
  for d in DISTRICTS:
    if d in address.lower():
      return DISTRICTS[d]
  return 0

def get_district_from_id(id: int):
  for d in DISTRICTS:
    if DISTRICTS[d] == id:
      return d
  return None

def get_sum_quantity_in_product(product: dict, size_id: str = ""):
  result = 0
  if 'variations' in product:
    if (size_id != ""):
      if convert_id_size(id_or_size = size_id) == "m" or convert_id_size(id_or_size = size_id) == "l":
        for v in product['variations']:
          if v['attributes'][0] == size_id:
            if ('quantity' in v):
              return v['quantity']
            return 0
        return -1
    else:
      for v in product['variations']:
        if ('quantity' in v):
          result += v['quantity']
      return result
  else:
    return product['quantity']

  return None

def sort_quan_product(all_products, limit: int):
  for p in all_products:
    p['sum'] = get_sum_quantity_in_product(p)
    # print(p['name'], p['sum'], '\n')
  if limit < len(all_products):
    return sorted(all_products, key = lambda k:k['sum'], reverse=True)[:limit]
  return sorted(all_products, key = lambda k:k['sum'], reverse=True)


def check_if_product_exist(all_products, product_name, size: str = ""):
  product = get_product(all_products, product_name)
  if (get_sum_quantity_in_product(product = product, size_id = convert_id_size(id_or_size = size)) > 0):
    return True
  return False

def get_sale_products(all_products):
  sale_products = []
  for product in all_products:
    if (product['name'].lower() in SALE_PRODUCTS):
      product['sale'] = SALE_PRODUCTS[product['name'].lower()]
      sale_products.append(product)
  return sale_products

def check_sale_product(product):
  if product['name'].lower() in SALE_PRODUCTS:
    product['sale'] = SALE_PRODUCTS[product['name'].lower()]
  return product
