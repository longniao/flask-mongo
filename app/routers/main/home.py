# -*- coding: utf-8 -*-

from flask import jsonify

from . import main_blueprint


@main_blueprint.route('/')
def index():
    return jsonify({'msg': 'Hello World!'})