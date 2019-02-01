#!/usr/local/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from app import ZaloMgr
from flask_mysqldb import MySQL
from app import config

app = Flask(__name__)
# app.config['MYSQL_USER'] = config.user
# app.config['MYSQL_PASSWORD'] = config.passwd
# app.config['MYSQL_DB'] = config.db
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# mysql = MySQL(app)
port = '5000'
# cur = mysql.connection.cursor()

@app.route('/')
def response_user_message():
  return ZaloMgr.reply();
