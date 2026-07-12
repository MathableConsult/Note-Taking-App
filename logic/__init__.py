# Converting all the modules into a package by adding __init__ file
# This will give us cleaner imports in app.py 
# and also make it easier to manage the codebase as it grows.

from .cRUD_oPERATIONS import *
from .db_config import db_config
