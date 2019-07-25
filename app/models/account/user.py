# -*- coding: utf-8 -*-

import arrow
from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager
from app.models.base.counter import Counter
from app.models.account import Role, Permission

default_user_info = dict(
    first_name='',
    last_name='',
)

class User(UserMixin, db.Document):
    user_id = db.IntField(required=True)
    user_name = db.StringField(required=True, max_length=100)
    email = db.StringField(max_length=200)
    password_hash = db.StringField(requied=True)
    timezone = db.StringField(requied=True, max_length=6)
    user_info = db.DictField(requied=True)
    role_id = db.IntField(required=True)
    confirmed = db.BooleanField(required=True, default=False)
    must_change_password = db.BooleanField(required=True, default=False)
    banned = db.BooleanField(required=True, default=False)
    suspended = db.BooleanField(required=True, default=False)
    created_time = db.DateTimeField(required=True, default=arrow.utcnow().datetime)
    updated_time = db.DateTimeField(required=True, default=arrow.utcnow().datetime)

    meta = {'db_alias': 'account', 'collection': 'user', 'allow_inheritance': True}

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def save(self):
        if not self.user_id:
            self.user_id = Counter.get_id('user')
        if not self.user_info:
            self.user_info = default_user_info
        super(User, self).save()

    def to_json(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "email": self.email,
            "timezone": self.timezone,
            "role_id": self.role_id,
            "confirmed": self.confirmed,
            "must_change_password": self.must_change_password,
            "banned": self.banned,
            "suspended": self.suspended,
            "created_time": self.created_time,
            "updated_time": self.updated_time,
        }

    @property
    def role(self):
        return Role.objects(role_id=self.role_id, enable=True).first()

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

    def full_name(self):
        return '%s %s' % (self.user_info.first_name, self.user_info.last_name)

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous(self):
        return False

    def is_confirmed(self):
        return self.confirmed

    def is_must_change_password(self):
        return self.must_change_password

    def is_banned(self):
        return self.banned

    def is_suspended(self):
        return self.suspended

    def get_id(self):
        return str(self.user_id)

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=604800):
        """Generate a confirmation token to email a new user."""

        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.user_id})

    def generate_email_change_token(self, new_email, expiration=3600):
        """Generate an email change token to email an existing user."""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.user_id, 'new_email': new_email})

    def generate_password_reset_token(self, expiration=3600):
        """
        Generate a password reset change token to email to an existing user.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.user_id})

    def confirm_account(self, token):
        """Verify that the provided token is for this user's id."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('confirm') != self.user_id:
            return False
        self.confirmed = True
        self.save()
        return True

    def change_email(self, token):
        """Verify the new email for this user."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('change_email') != self.user_id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.objects(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        db.session.commit()
        return True

    def reset_password(self, token, new_password):
        """Verify the new password for this user."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        self.save()
        return True

    def __repr__(self):
        return '<User \'%s %s\'>' % (self.user_id, self.user_name)


class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.objects(user_id=int(user_id)).all()
