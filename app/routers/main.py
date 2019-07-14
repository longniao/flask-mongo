# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

main = Blueprint('main', __name__)

from flask import jsonify

@main.route('/')
def index():
    return jsonify({'msg': 'Hello World!'})