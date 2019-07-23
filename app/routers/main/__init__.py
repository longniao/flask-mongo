# -*- coding: utf-8 -*-

from flask import Blueprint

main_blueprint = Blueprint('main', __name__)


from .index import *
from .about import *

