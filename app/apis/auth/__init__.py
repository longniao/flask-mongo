# -*- coding: utf-8 -*-

from flask import Blueprint

auth_blueprint = Blueprint('auth', __name__)


from .login import *
from .register import *
