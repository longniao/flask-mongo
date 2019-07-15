# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return jsonify({'msg': 'Hello World!'})