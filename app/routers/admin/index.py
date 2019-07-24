# -*- coding: utf-8 -*-

from flask import render_template
from flask_login import current_user, login_required

from app.library.decorators import admin_required
from . import admin_blueprint


@admin_blueprint.route('/')
@login_required
@admin_required
def index():
    return render_template('admin/index.html')

