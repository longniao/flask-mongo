# -*- coding: utf-8 -*-

import arrow

from app import db
from app.models.base.counter import CounterMixin


class Permission:
    GENERAL = 0x01
    ADMINISTER = 0xff

class Role(db.Document):
    role_id = db.IntField(required=True)
    role_name = db.StringField(required=True, max_length=100)
    index = db.StringField(required=True)
    permissions = db.IntField(required=True, max_length=11, default=0)
    enable = db.BooleanField(required=True, default=True)
    createtime = db.DateTimeField(required=True, default=arrow.utcnow().datetime)

    meta = {'collection': 'role', 'allow_inheritance': True}

    def to_json(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "permissions": self.permissions,
        }

    def get_id(self):
        return str(self.role_id)

    def get_name(self):
        return str(self.role_name)

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.GENERAL, 'main', True),
            'Administrator': (
                Permission.ADMINISTER,
                'admin',
                False  # grants all permissions
            )
        }
        roles = Role.objects.first()
        print('roles:', roles.__dict__)
        return False
        for r in roles:
            role = Role.objects(role_name=r).first()
            print('role:', role.explain())
            if role is None:
                print('None')
                role = Role(role_name=r)
            role.role_id = roles[r][0]
            role.index = roles[r][1]
            role.enable = roles[r][2]
            print(role.__dict__)
            role.save()
