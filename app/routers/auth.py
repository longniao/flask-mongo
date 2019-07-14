# -*- coding: utf-8 -*-

from datetime import datetime

from flask import (
    Blueprint,
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

from app.models.user import User
from app.utils.email import send_email

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def registerUser():
    if not request.json or not 'name' in request.json or not 'pwd' in request.json:
        return jsonify({'err': 'Request not Json or miss name/pwd'})
    elif User.objects(name=request.json['name']).first():
        return jsonify({'err': 'Name is already existed.'})
    else:
        user = User(
            user_id=User.objects().count() + 1,
            name=request.json['name'],
            email=request.json['email'] if 'email' in request.json else "",
            pwd=request.json['pwd'],
            createtime=datetime.now()
        )
        try:
            user.save()
            login_user(user)
        except Exception as e:
            print(e)
            return jsonify({'err': 'Register error.'})
    return jsonify({'status': 0, 'user_id': user['user_id'], 'msg': 'Register success.'})


@auth.route('/login', methods=['POST'])
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


@auth.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'status': 0, 'msg': 'Logout success.'})
