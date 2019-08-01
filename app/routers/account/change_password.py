# -*- coding: utf-8 -*-

from app.services.account.forms import ChangePasswordForm
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
from flask_babel import lazy_gettext as _

from . import account_blueprint


@account_blueprint.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change an existing user's password."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash(_('Your password has been updated.'), 'form-success')
            return redirect(url_for('main.index'))
        else:
            flash(_('Original password is invalid.'), 'form-error')
    return render_template('account/manage.html', form=form)


