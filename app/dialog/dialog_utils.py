from app.dialog.const import START_STATE, ORDER_INTENT, ORDERING_STATE

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
  return dialog

def update_snips(dialog: dict, msg: str, intent: list, entities: list):
  dialog["snips"]["sentence"] = msg
  dialog["snips"]["intent"] = intent
  update_entities(dialog = dialog, entities = entities)
  # for entity in entities:
  #   new_entity = {
  #     "label": entity['type'],
  #     "value": entity['text']
  #   }
  #   dialog["snips"]['entities'].append(new_entity)

  return dialog

def update_entities(dialog: dict, entities: list):
  new_entities = []
  for entity in entities:
    new_entity = {
      "label": entity['type'],
      "value": entity['text']
    }
    # Update entites

    # is_new = True
    # for old_entity in dialog['snips']['entities']:
    #   if old_entity["label"] == new_entity["label"]
    # Tam thoi chi insert tren cung
    new_entities.append(new_entity)
  dialog['snips']['entities'].insert(0, new_entities)
  return dialog

def check_missing_entity(dialog: dict, intent: str):
  entities = dialog['snips']['entities'][0]
  # Check missing entity in order section
  if (intent == ORDER_INTENT or intent == ORDERING_STATE):
    return dialog
  return dialog
