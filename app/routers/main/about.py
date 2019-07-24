# -*- coding: utf-8 -*-

from flask import render_template
from flask_login import current_user

from . import main_blueprint


@main_blueprint.route('/about')
def about():
    return render_template('main/about.html', editable_html_obj='')
