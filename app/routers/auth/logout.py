# -*- coding: utf-8 -*-

from flask import (
    flash,
    redirect,
    url_for,
)
from flask_login import (
    logout_user,
)
from flask_babel import lazy_gettext as _

from . import auth_blueprint


@auth_blueprint.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash(_('You have been logged out.'), 'info')
    return redirect(url_for('main.index'))
