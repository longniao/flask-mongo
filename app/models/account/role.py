# -*- coding: utf-8 -*-

import arrow

from app import db
from app.models.base.counter import Counter
from app.models.account import Permission


class Role(db.Document):
    role_id = db.IntField(required=True)
    role_name = db.StringField(required=True, max_length=100)
    index = db.StringField(required=True)
    permissions = db.IntField(required=True, max_length=11, default=0)
    default = db.BooleanField(required=True, default=False)
    enable = db.BooleanField(required=True, default=True)
    createtime = db.DateTimeField(required=True, default=arrow.utcnow().datetime)

    meta = {'db_alias': 'account', 'collection': 'role', 'allow_inheritance': True}

    def save(self):
        if self.role_id is None:
            self.role_id = Counter.get_id('role')
        super(Role, self).save()

    def to_json(self):
        return {
            "role_id": self.role_id,
            "role_name": self.role_name,
            "index": self.index,
            "permissions": self.permissions,
        }

    def get_id(self):
        return str(self.role_id)

    def get_name(self):
        return str(self.role_name)

    @staticmethod
    def insert_roles():
        roles = dict(
            User=dict(
                permission=Permission.GENERAL,
                index='main',
                default=True,
                enable=True,
            ),
            Administrator=dict(
                permission=Permission.ADMINISTER,
                index='admin',
                default=False,
                enable=True,
            )
        )
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }

        for k, v in roles.items():
            role = Role.objects(role_name=k).first()
            if role is None:
                role = Role(role_name=k)
            role.permission = v['permission']
            role.index = v['index']
            role.default = v['default']
            role.enable = v['enable']
            role.save()
