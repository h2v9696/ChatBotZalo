#!/usr/local/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from app.dialog.dialog_manager import DialogManager
from flask_mysqldb import MySQL
from app import config

app = Flask(__name__)
dialogManager = DialogManager()

# app.config['MYSQL_USER'] = config.user
# app.config['MYSQL_PASSWORD'] = config.passwd
# app.config['MYSQL_DB'] = config.db
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# mysql = MySQL(app)
port = '5000'
# cur = mysql.connection.cursor()

@app.route('/', methods=['GET', 'POST'])
def response_user_message():
  if request.method == 'POST':
    return 'OK';
  else:
    dialogManager.reply();
    return 'OK';

# @app.route('/', methods=['GET', 'POST'])
# def response_user_message():
#   return "OK";
