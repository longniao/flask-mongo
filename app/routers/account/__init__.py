# -*- coding: utf-8 -*-

from flask import Blueprint

account_blueprint = Blueprint('account', __name__)


from .manage import *
