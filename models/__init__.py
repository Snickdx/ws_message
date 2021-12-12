from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .user import *
from .post import *
from .subscription import *
from .topic import *
from .inbox import *