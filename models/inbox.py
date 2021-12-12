import enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Inbox(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer, primary_key=True)
    read = db.Column(db.Boolean, default=False)
    notified = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"{self.text}"
 
    def toDict(self):
        return {
            "userId": self.userId,
            "postId": self.postId,
            "read":self.read,
            "notified":self.notified
        }