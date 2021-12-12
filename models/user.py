from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # feed = db.relationship('Post', secondary=Inbox, lazy='subquery', backref=db.backref('recipients', lazy=True))
    # subbed_topics = db.relationship('Topic', secondary=Subscription, lazy='subquery', backref=db.backref('subscribers', lazy=True))
    sid = None

    def toDict(self):
      return {
        "id": self.id,
        "username": self.username
      }

    # def get_topics_json(self):
    #   return [ topic.toDict() for topic in self.subbed_topics]

    def get_feed_json(self):
      # return [ post.toDict() for post in self.feed ]
      return []
      
    def get_sid(self):
      return self.sid

    def set_sid(self, sid):
      self.sid = sid
    
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)