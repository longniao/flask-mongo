# -*- coding: utf-8 -*-

from app.library.email import send_email
from app.models.account import User
from app.services.auth.forms import RequestResetPasswordForm, ResetPasswordForm
from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user
from flask_rq import get_queue
from flask_babel import lazy_gettext as _

from . import auth_blueprint


@auth_blueprint.route('/reset-password', methods=['GET', 'POST'])
def forgot_password_request():
    """Respond to existing user's request to reset their password."""
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user:
            token = user.generate_password_reset_token()
            reset_link = url_for(
                'account.reset_password', token=token, _external=True)
            get_queue().enqueue(
                send_email,
                recipient=user.email,
                subject=_('Reset Your Password'),
                template='account/email/reset_password',
                user=user,
                reset_link=reset_link,
                next=request.args.get('next'))
        flash(_('A password reset link has been sent to {}.').format(
            form.email.data), 'warning')
        return redirect(url_for('auth.login'))
    return render_template('account/reset_password.html', form=form)


@auth_blueprint.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset an existing user's password."""
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user is None:
            flash('Invalid email address.', 'form-error')
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.new_password.data):
            flash('Your password has been updated.', 'form-success')
            return redirect(url_for('account.login'))
        else:
            flash('The password reset link is invalid or has expired.',
                  'form-error')
            return redirect(url_for('main.index'))
    return render_template('account/reset_password.html', form=form)
