# -*- coding: utf-8 -*-

from app import db


class Permission:
    GENERAL = 0x01
    ADMINISTER = 0xff

class Role(db.Document):
    role_id = db.IntField(required=True)
    role_name = db.StringField(required=True, max_length=100)
    role_email = db.StringField(max_length=200)
    createtime = db.DateTimeField(required=True)

    def to_json(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email
        }

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)

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
        for r in roles:
            role = Role.objects(name=r).first()
            if role is None:
                role = Role(name=r)
            role.role_id = roles[r][0]
            role.index = roles[r][1]
            role.default = roles[r][2]
            role.save()

    def __repr__(self):
        return '<Role \'%s\'>' % self.name