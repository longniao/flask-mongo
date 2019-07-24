# -*- coding: utf-8 -*-

from app.routers.account import account_blueprint
from app.routers.auth import auth_blueprint
from app.routers.main import main_blueprint
from app.routers.admin import admin_blueprint
from app.routers.todo import todo as todo_blueprint


__all__ = [
    'account_blueprint',
    'auth_blueprint',
    'admin_blueprint',
    'main_blueprint',
    'task_blueprint',
]
