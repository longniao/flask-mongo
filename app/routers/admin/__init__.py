# -*- coding: utf-8 -*-

from flask import Blueprint

admin_blueprint = Blueprint('admin', __name__)

from .index import *
from .update_editor_contents import *
