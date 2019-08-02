# -*- coding: utf-8 -*-

from flask import (
    redirect,
    url_for,
    request,
    Blueprint,
)

account_blueprint = Blueprint('account', __name__)


from .index import *
from .manage import *
from .change_email import *
from .change_password import *
from .confirm import *


@account_blueprint.route('/unconfirmed')
def unconfirmed():
    """Catch users with unconfirmed emails."""
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('account/unconfirmed.html')


@account_blueprint.before_app_request
def before_request():
    """Force user to confirm email before accessing login-required routes."""
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint[:8] != 'account.' \
            and request.endpoint != 'static':
        return redirect(url_for('account.unconfirmed'))
