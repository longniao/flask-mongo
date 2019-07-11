# -*- coding: utf-8 -*-

from .. import db, login_manager

class Task(db.Document):
    task_id = db.StringField(required=True)
    title = db.StringField(required=True, max_length=50)
    description = db.StringField(required=True, max_length=1000)
    done = db.BooleanField(required=True)
    createtime = db.DateTimeField(required=True)
    completetime = db.DateTimeField()

    def to_json(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "createtime": self.createtime.strftime("%Y-%m-%d %H:%M:%S"),
            "completetime": self.completetime.strftime("%Y-%m-%d %H:%M:%S") if self.done else ""
        }

