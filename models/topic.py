from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from .subscription import Subscription, Status
# from .user import User
# from .inbox import Inbox

import enum

class Level(enum.Enum):
    ZERO = "ZERO"
    ONE = "ONE"

    def __str__(self):
      return '%s' % self.value

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    level = db.Column(db.Enum(Level), default=Level.ZERO)
  
    # def get_active_subscribers(self):
    #   subs = Subscription.query.filter_by(topicId=self.id, status=Status.ACTIVE)
    #   userIds = [ sub.userId for sub in subs ]
    #   users = User.query.filter(User.id.in_(userIds))
    #   return users

    def __init__(self, text):
        self.text = text

    def subscribe(self, userId):
        sub = Subscription.query.filter_by(userId=userId, topicId=self.id).first()
        if sub :
          sub.set_active()
        else :
          sub = Subscription(userId=userId, topicId=self.id)
        db.session.add(sub)
        db.session.commit()

    # def num_subscribers(self):
    #   return len(self.subscribers)

    # def new_post(self, postId):
    #   subs = self.get_active_subscribers()
    #   for user in subs:
    #     message = Inbox(userId=user.id, postId=postId)
    #     db.session.add(message)
    #   db.session.commit()
    #   return len(subs)

    # def unsubscribe(self, userId):
    #     sub = Subscription.query.filter_by(userId=userId, topicId=self.id).first()
    #     if sub :
    #       sub.set_inactive()
          
    def toDict(self):
        return {
          "id": self.id,
          "text": self.text,
          "level": str(self.level)
        }