from app.dialog.const import START_STATE, ORDER_INTENT, ORDERING_STATE, \
                                                ORDERING_STATE_ADD, ORDERING_STATE_SWAP

# """
# dialog : {
#     'user_id': 0,
#     'state': "",
#     "snips":[
#                 {
#                    "sentence": "Hom nay toi buon cho 3 chai votka di",
#                    "intent": "order"
#                    "entity": [{
#                        'label': "address",
#                        'value': "Hai Ba Trung"
#                    }]
#                 }
#             ],
#     'responses':[
#                 {
#                     reply_type: "",
#                     reply: "",
#                     sub_reply: "",
#                     image_url: '',
#                     links: [],
#                     button: ""
#                 },
#             ],
#     Luu them nhien bien can truyen qua state
#     variable:{}
# }
# """

# class DialogInfo:
#   @staticmethod
def create_dialog(user_id):
    """
    Create dialog
    :param user_id: id
    :return:
    """
    dialog = {}
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

# @staticmethod
def set_response(dialog: dict, response: str):
  dialog["responses"] = response
  return dialog

# @staticmethod
def get_state(dialog: dict):
  return dialog['state']

# @staticmethod
def set_state(dialog: dict, state: str):
  dialog['state'] = state
  if state == START_STATE:
    dialog['variable'] = {}
    dialog['snips']['entities'] = []

  return dialog

def update_snips(dialog: dict, msg: str, intent: list, entities: list):
  dialog["snips"]["sentence"] = msg
  dialog["snips"]["intent"] = intent
  current_state = get_state(dialog)
  # if (current_state == ORDERING_STATE_SWAP):
  #   update_entities(dialog = dialog, entities = entities)
  # else:
  if (len(entities) > 0):
    add_entities(dialog = dialog, entities = entities)
  # for entity in entities:
  #   new_entity = {
  #     "label": entity['type'],
  #     "value": entity['text']
  #   }
  #   dialog["snips"]['entities'].append(new_entity)

  return dialog

def add_entities(dialog: dict, entities: list):
  new_entities = []
  for entity in entities:
    new_entity = {
      "label": entity['type'],
      "value": entity['text'],
      "parent": ""
    }
    # Entities cua 1 intent moi
    new_entities.append(new_entity)
  # if (len(dialog['snips']['entities']) > 0):
  #   dialog['snips']['entities'].pop(0)
  # Set TYPE as a parent of it's attributes
  new_entities = __set_entities_parent(entities = new_entities)
  dialog['snips']['entities'].insert(0, new_entities)
  return dialog

def __set_entities_parent(entities: list):
  # Set TYPE as a parent of it's attributes
  for index, entity in enumerate(entities):
    if (entity['label'] == "TYPE"):
      if (index < len(entities) - 1):
        i = index + 1
        while (entities[i]['label'] == 'SIZE' or entities[i]['label'] == 'TOPPING'
          or entities[i]['label'] == 'ADJUSTICE' or entities[i]['label'] == 'ADJUSTSUGAR'):
          entities[i]['parent'] = entity['value']
          i += 1
          if (i >= len(entities)):
            break
      if (index > 0):
        i = index - 1
        while ((entities[i]['label'] == 'QUANTITY' or entities[i]['label'] == 'SIZE' or entities[i]['label'] == 'TOPPING'
          or entities[i]['label'] == 'ADJUSTICE' or entities[i]['label'] == 'ADJUSTSUGAR') and entities[i]['parent'] == ''):
          entities[i]['parent'] = entity['value']
          i -= 1
          if (i < 0):
            break

  return entities

def update_entities(dialog: dict, entities: list, last_entity: dict = None):
  old_entities = dialog['snips']['entities'][0]
  current_state = get_state(dialog)

  new_entities = []
  index = 0
  for entity in entities:
    new_entity = {
      "label": entity['label'],
      "value": entity['value'],
      "parent": entity['parent']
    }
    # Update or add new at first entites
    is_new = True
    for old_entity in old_entities:
      if (current_state == ORDERING_STATE_SWAP and old_entity["label"] == new_entity["label"]):
        print(last_entity, old_entity, new_entity, '\n')
        if (last_entity != None and old_entity["value"] == last_entity["value"]):
          print("WAT")
          old_entity["value"] = new_entity["value"]
          is_new = False
          if (old_entity["label"] == "TYPE"):
            old_entities = __set_entities_parent(entities = old_entities)
          # if old_entity["label"] == "TYPE":
          break

        if (last_entity == None):
          old_entity["value"] = new_entity["value"]

    if is_new:
      old_entities.append(new_entity)
      # Temporarity append later: 'SIZE' 'TOPPING' 'ADJUSTICE' 'ADJUSTSUGAR' need to be behind 'TYPE'
      # and
      #   (new_entity["label"]  != "TYPE" or new_entity["label"]  != "TOPPING" or new_entity["label"]  != "SIZE" or
      #     new_entity["label"]  != "ADJUSTICE" or new_entity["label"]  != "ADJUSTSUGAR")
  return dialog

def check_missing_entity(dialog: dict, intent: str):
  entities = dialog['snips']['entities'][0]
  missing_entities = []
  # Check missing entity in order section
  if (intent == ORDER_INTENT or intent == ORDERING_STATE):
    # Full entity TYPE PHONE LOCATION
    countPhone = 0
    countLoc = 0
    for entity in entities:
      if entity['label'] == 'PHONE':
        countPhone += 1
      if entity['label'] == 'LOCATION':
        countLoc += 1
    if countPhone == 0:
      missing_entities.append('PHONE')
    if countLoc == 0:
      missing_entities.append('LOCATION')

  return missing_entities
