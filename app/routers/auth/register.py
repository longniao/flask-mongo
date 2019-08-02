# -*- coding: utf-8 -*-

from app.library.email import send_email
from app.services.auth.forms import (
    RegistrationForm,
)
from flask import (
    flash,
    redirect,
    render_template,
    url_for,
)
from flask_rq import get_queue
from werkzeug.security import generate_password_hash
from flask_babel import lazy_gettext as _

from app.models.account import User, Role
from . import auth_blueprint


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user, and send them a confirmation email."""
    form = RegistrationForm()
    if form.validate_on_submit():
        role = Role.objects(default=True, enable=True).first()
        if role is not None:
            role_id = role.pkid
        else:
            role_id = 1
        user = User(
            user_name=form.user_name.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role_id=role_id
        )
        user.save()
        token = user.generate_confirmation_token()
        confirm_link = url_for('account.confirm', token=token, _external=True)
        get_queue().enqueue(
            send_email,
            recipient=user.email,
            subject=_('Confirm Your Account'),
            template='account/email/confirm',
            user=user,
            confirm_link=confirm_link)
        flash(_('A confirmation link has been sent to {}.').format(user.email), 'warning')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)
