#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from zalo.sdk.oa import ZaloOaInfo, ZaloOaClient
import json
from app import config
from app.engine.main_bot import BotManager

app = Flask(__name__)
port = '5000'

zalo_info = ZaloOaInfo(oa_id=config.oaid, secret_key=config.secretKey)
zalo_oa_client = ZaloOaClient(zalo_info)

@app.route('/')
def response_user_message():
  msg = request.args.get('message')
  user_id = request.args.get('fromuid')
  # User profile
  profile = zalo_oa_client.get('getprofile', {'uid': user_id})
  # print (profile['data']['displayName'])
  # message_status = zalo_oa_client.get('getmessagestatus', {'msgid': request.args.get('msgid')})
  # print(message_status)

  data = {
      'uid': user_id,
      'message': BotManager.reply(msg)
      # 'message': 'Chào bạn ' + profile['data']['displayName']
  }
  params = {'data': data}
  send_text_message = zalo_oa_client.post('sendmessage/text', params)
  return msg

