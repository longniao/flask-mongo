# -*- coding: utf-8 -*-

from app import db


class Counter(db.Document):
    _id = db.StringField(required=True)
    next = db.IntField(required=True)

    def to_json(self):
        return {
            "_id": self._id,
            "next": self.next,
        }

    def get_id(self, name = '_defalut_'):
        counter = Counter.objects(_id=name).update_one(set__next=1, upsert=True)
        return counter.next

    def __repr__(self):
        return '<Counter name:\'%s\', next:\'%s\'>' % (self._id, self.next)