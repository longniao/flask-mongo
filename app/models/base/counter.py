# -*- coding: utf-8 -*-

from app import db


class Counter(db.Document):
    name = db.StringField(required=True)
    next_id = db.IntField(required=True)

    meta = {'db_alias': 'base', 'collection': 'counter', 'allow_inheritance': True}

    def to_json(self):
        return {
            "name": self.name,
            "next_id": self.next_id,
        }

    @staticmethod
    def get_id(name = '_defalut_'):
        Counter.objects(name=name).modify(upsert=True, new=True, inc__next_id=1)
        return Counter.objects(name=name).first().next_id

    def __repr__(self):
        return '<Counter name:\'%s\', next_id:\'%s\'>' % (self.name, self.next_id)