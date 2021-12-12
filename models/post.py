from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    topicId = db.Column(db.Integer, db.ForeignKey('topic.id'))
    text = db.Column(db.String(200), nullable=False) 
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.userId}"

    def toDict(self):
        return {
            "userId": self.userId,
            "topicId": self.topicId,
            "text": self.text,
            "created": self.created
        }