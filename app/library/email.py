# -*- coding: utf-8 -*-

import os

from flask import render_template
from flask_mail import Message

from app import create_app
from app import mail


def send_email(recipient, subject, template, **kwargs):
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    with app.app_context():
        msg = Message(
            app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
            sender=app.config['MAIL_SENDER'],
            recipients=[recipient])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)
