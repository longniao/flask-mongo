# -*- coding: utf-8 -*-

from flask import Blueprint

account_blueprint = Blueprint('account', __name__)


from .index import *
from .manage import *
from .change_email import *
from .change_password import *
