# -*- coding: utf-8 -*-

from app.routers.account import account as account_blueprint
from app.routers.auth import auth as auth_blueprint
from app.routers.main import main as main_blueprint
from app.routers.todo import todo as todo_blueprint


__all__ = [
    'account_blueprint',
    'auth_blueprint',
    'main_blueprint',
    'todo_blueprint',
]
