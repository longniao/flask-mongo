# -*- coding: utf-8 -*-

from flask import (
    flash,
    redirect,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
)
from flask_babel import lazy_gettext as _

from . import auth_blueprint


@auth_blueprint.route('/confirm/<token>')
@login_required
def confirm(token):
    """Confirm new user's account with provided token."""
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm_account(token):
        flash(_('Your account has been confirmed.'), 'success')
    else:
        flash(_('The confirmation link is invalid or has expired.'), 'error')
    return redirect(url_for('main.index'))