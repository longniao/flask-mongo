# -*- coding: utf-8 -*-

from app import app

from flask import jsonify

@app.route('/')
def index():
    return jsonify({'msg': 'Hello World!'})