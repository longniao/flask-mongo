# -*- coding: utf-8 -*-

from flask import render_template, request
from flask_login import current_user, login_required

from app.library.decorators import admin_required
from . import admin_blueprint


@admin_blueprint.route('/update_editor_contents', methods=['POST'])
@login_required
@admin_required
def update_editor_contents():
    """Update the contents of an editor."""

    edit_data = request.form.get('edit_data')
    editor_name = request.form.get('editor_name')

    return 'OK', 200
