import enum
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Status(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

    def __str__(self):
      return '%s' % self.value

class Subscription(db.Model):

    userId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    topicId = db.Column(db.Integer, db.ForeignKey('topic.id'), primary_key=True, )
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.Enum(Status), default=Status.ACTIVE)

    def __init__(self, userId, topicId):
        self.userId = userId
        self.topicId = topicId

    def __repr__(self):
        return f"{self.user_id}"

    def set_active(self):
        self.status = Status.ACTIVE

    def set_inactive(self):
        self.status = Status.INACTIVE

    def get_created_string(self):
        return self.created.strftime("%m/%d/%Y, %H:%M:%S")

    def toDict(self):
        return {
            "id":self.id,
            "userId": self.userId,
            "topicId": self.topicId,
            "created": self.get_created_string(),
            "satus": str(self.status)
        }