# -*- coding: utf-8 -*-

import arrow

from app import db
from app.models.base.counter import Counter
from app.models.account import Permission


class Role(db.Document):
    pkid = db.IntField(required=True)
    name = db.StringField(required=True, max_length=100)
    index = db.StringField(required=True)
    permissions = db.DictField(required=True)
    default = db.BooleanField(required=True, default=False)
    enable = db.BooleanField(required=True, default=True)
    createtime = db.DateTimeField(required=True, default=arrow.utcnow().datetime)

    meta = {'db_alias': 'account', 'collection': 'role', 'allow_inheritance': True}

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = Permission().to_json()

    def save(self):
        if self.pkid is None:
            self.pkid = Counter.get_id('role')
        super(Role, self).save()

    def to_json(self):
        return {
            "pkid": self.pkid,
            "name": self.name,
            "index": self.index,
            "permissions": self.permissions,
        }

    def get_pkid(self):
        return str(self.pkid)

    @staticmethod
    def insert_roles():
        permissions = Permission().to_json()
        roles = dict()
        roles['User'] = dict(
            permissions=permissions,
            index='account',
            default=True,
            enable=True,
        )

        permissions['content_audit'] = True
        permissions['content_manage'] = True
        roles['Manager'] = dict(
            permissions=permissions,
            index='admin',
            default=False,
            enable=True,
        )

        permissions['account_manage'] = True
        permissions['administer'] = True
        roles['Administrator'] = dict(
            permissions=permissions,
            index='admin',
            default=False,
            enable=True,
        )

        for k, v in roles.items():
            role = Role.objects(name=k).first()
            if role is None:
                role = Role(name=k)
            role.permissions = v['permissions']
            role.index = v['index']
            role.default = v['default']
            role.enable = v['enable']
            role.save()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions[perm] = True

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions[perm] = False

    def reset_permissions(self):
        self.permissions = Permission().to_json()

    def has_permission(self, perm):
        return self.permissions[perm]

    def __repr__(self):
        return '<Role %r>' % self.name