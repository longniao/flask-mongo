# -*- coding: utf-8 -*-

from flask import jsonify
from flask import render_template

from . import main_blueprint


@main_blueprint.route('/')
def index():
    return jsonify({'msg': 'Hello World!'})


@main_blueprint.route('/about')
def about():
    return render_template('main/about.html', editable_html_obj='')
