# -*- coding: utf-8 -*-

import arrow

from app import db


class User(db.Document):
    user_id = db.IntField(required=True)
    user_name = db.StringField(required=True, max_length=100)
    email = db.StringField(max_length=200)
    password = db.StringField(requied=True)
    timezone = db.StringField(requied=True, max_length=6)
    user_info = db.DictField(requied=True)
    confirmed = db.BooleanField(required=True, default=False)
    must_change_password = db.BooleanField(required=True, default=False)
    banned = db.BooleanField(required=True, default=False)
    suspended = db.BooleanField(required=True, default=False)
    created_time = db.DateTimeField(required=True, default=arrow.utcnow().datetime)
    updated_time = db.DateTimeField(required=True, default=arrow.utcnow().datetime)

    def to_json(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "email": self.email,
            "timezone": self.timezone,
            "confirmed": self.confirmed,
            "must_change_password": self.must_change_password,
            "banned": self.banned,
            "suspended": self.suspended,
            "created_time": self.created_time,
            "updated_time": self.updated_time,
        }

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

    def get_user_info(self):
        return self.user_info
