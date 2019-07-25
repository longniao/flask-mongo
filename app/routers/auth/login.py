# -*- coding: utf-8 -*-

from app.models.account import User
from app.services.auth.forms import (
    LoginForm,
)
from flask import (
    jsonify,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    login_user,
    logout_user,
)

from . import auth_blueprint


@auth_blueprint.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        print(user.to_json())
        if user is not None and user.password_hash is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('You are now logged in. Welcome back!', 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Invalid email or password.', 'form-error')
    return render_template('auth/login.html', form=form)
