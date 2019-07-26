# -*- coding: utf-8 -*-

from flask import (
    redirect,
    url_for,
)
from flask_login import login_required

from . import account_blueprint


@account_blueprint.route('/')
@login_required
def index():
    """Display a user's account information."""
    return redirect(url_for('account.manage'))

