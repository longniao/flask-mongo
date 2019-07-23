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


@auth_blueprint.route('/login', methods=['POST'])
def login():
    if not request.json or not 'name' in request.json or not 'pwd' in request.json:
        return jsonify({'err': 'Request not Json or miss name/pwd'})
    else:
        user = User.objects(
            name=request.json['name'], pwd=request.json['pwd']).first()
    if user:
        login_user(user)
        return jsonify({'status': 0, 'user_id': user.get_id(), 'msg': 'Login success.'})
    else:
        return jsonify({'err': 'Login fail.'})


@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'status': 0, 'msg': 'Logout success.'})
