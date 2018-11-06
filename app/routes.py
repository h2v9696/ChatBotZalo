#!/usr/local/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from app import ZaloMgr
app = Flask(__name__)
port = '5000'

@app.route('/')
def response_user_message():
  return ZaloMgr.reply();
