# -*- coding: utf-8 -*-

from flask import (
    flash,
    redirect,
    render_template,
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
from app.services.account.forms import ChangeEmailForm


@account_blueprint.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    """Respond to existing user's request to change their email."""
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            change_email_link = url_for('account.change_email', token=token, _external=True)
            get_queue().enqueue(
                send_email,
                recipient=new_email,
                subject=_('Confirm Your New Email'),
                template='account/email/change_email',
                # current_user is a LocalProxy, we want the underlying user
                # object
                user=current_user._get_current_object(),
                change_email_link=change_email_link)

            flash(_('A confirmation link has been sent to {}.').format(new_email),
                  'warning')
            return redirect(url_for('account.index'))
        else:
            flash(_('Invalid email or password.'), 'form-error')
    return render_template('account/manage.html', form=form)


@account_blueprint.route('/change-email/<token>', methods=['GET', 'POST'])
@login_required
def change_email(token):
    """Change existing user's email with provided token."""
    if current_user.change_email(token):
        flash(_('Your email address has been updated.'), 'success')
    else:
        flash(_('The confirmation link is invalid or has expired.'), 'error')
    return redirect(url_for('main.index'))
