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
from flask_rq import get_queue
from flask_babel import lazy_gettext as _

from . import account_blueprint
from app.library.email import send_email


@account_blueprint.route('/confirm')
@login_required
def confirm_request():
    """Respond to new user's request to confirm their account."""
    token = current_user.generate_confirmation_token()
    confirm_link = url_for('account.confirm', token=token, _external=True)
    get_queue().enqueue(
        send_email,
        recipient=current_user.email,
        subject='Confirm Your Account',
        template='account/email/confirm',
        # current_user is a LocalProxy, we want the underlying user object
        user=current_user._get_current_object(),
        confirm_link=confirm_link)
    flash('A new confirmation link has been sent to {}.'.format(
        current_user.email), 'warning')
    return redirect(url_for('main.index'))


@account_blueprint.route('/confirm/<token>')
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