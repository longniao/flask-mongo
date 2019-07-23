# -*- coding: utf-8 -*-

from datetime import datetime

from flask import (
    jsonify,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_rq import get_queue

from app import db
from app.services.auth.forms import (
    ChangeEmailForm,
    ChangePasswordForm,
    CreatePasswordForm,
    LoginForm,
    RegistrationForm,
    RequestResetPasswordForm,
    ResetPasswordForm,
)
from . import auth_blueprint
from app.models.account import User
from app.library.email import send_email


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user, and send them a confirmation email."""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            user_name=form.user_name.data,
            email=form.email.data,
            password_hash=form.password.data,
            role_id=1
        )
        user.save()
        token = user.generate_confirmation_token()
        confirm_link = url_for('auth.confirm', token=token, _external=True)
        get_queue().enqueue(
            send_email,
            recipient=user.email,
            subject='Confirm Your Account',
            template='account/email/confirm',
            user=user,
            confirm_link=confirm_link)
        flash('A confirmation link has been sent to {}.'.format(user.email),
              'warning')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)
