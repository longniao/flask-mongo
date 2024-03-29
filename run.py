#!/usr/bin/env python3

import os
import redis
import subprocess

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from rq import Connection, Queue, Worker
from werkzeug.security import generate_password_hash

from app import create_app, db

from app.models.account import Role, User
from config import Config, config_env

app = create_app(config_env)
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.option(
    '-n',
    '--number-users',
    default=10,
    type=int,
    help='Number of each model type to create',
    dest='number_users')
def add_fake_data(number_users):
    """
    Adds fake data to the database.
    """
    User.generate_fake(count=number_users)


@manager.command
def setup_dev():
    """Runs the set-up needed for local development."""
    setup_general()


@manager.command
def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()


def setup_general():
    """Runs the set-up needed for both local development and production.
       Also sets up first admin user."""
    Role.insert_roles()
    role_admin = Role.objects(name='Administrator').first()
    if role_admin is not None:
        if User.objects(email=Config.ADMIN_EMAIL).first() is None:
            user = User(
                user_name='admin',
                password_hash=generate_password_hash(Config.ADMIN_PASSWORD),
                role_id=role_admin.pkid,
                confirmed=True,
                email=Config.ADMIN_EMAIL,
                user_info=dict(
                    first_name='Admin',
                    last_name='Account',
                )
            )
            user.save()
            print('Added administrator {}'.format(user.to_json()))


@manager.command
def run_worker():
    """Initializes a slim rq task queue."""
    listen = ['default']
    redis_connection = redis.from_url(app.config['RQ_REDIS_URL'])
    with Connection(redis_connection):
        worker = Worker(map(Queue, listen))
        worker.work()


@manager.command
def format():
    """Runs the yapf and isort formatters over the project."""
    isort = 'isort -rc *.py app/'
    yapf = 'yapf -r -i *.py app/'

    print('Running {}'.format(isort))
    subprocess.call(isort, shell=True)

    print('Running {}'.format(yapf))
    subprocess.call(yapf, shell=True)


if __name__ == '__main__':
    manager.run()
