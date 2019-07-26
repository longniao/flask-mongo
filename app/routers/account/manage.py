# -*- coding: utf-8 -*-

from flask import render_template
from flask_login import current_user, login_required

from . import account_blueprint


@account_blueprint.route('/')
@account_blueprint.route('/manage')
@login_required
def manage():
    """Display a user's account information."""
    return render_template('account/manage.html', user=current_user, form=None)

