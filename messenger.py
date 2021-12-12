from flask_socketio import SocketIO, send, emit, disconnect, join_room
from models import db, User, Topic# Post, db, Post, Status

class Messenger:

  def new_post(self, userId, topicId, text):
    pass
    # post = Post(userId=userId, topicId=topicId, text=text)
    # db.session.add(post)
    # db.session.commit()
    # topic = Topic.query.get(topicId)
    # num_subs = topic.new_post(post.id)
    # self.broadcast(topic.text, {'postId':post.id, 'author':userId, 'topic':topic.text, 'topicId':topicId, 'text':text, 'created':post.created})
    # return num_subs


  def broadcast(self, topic, data):
    emit('message', data, room=topic, broadcast=True)

  def add_online_user(self, user, sid):
    join_room(user.sid)

  def remove_online_User(self, sid):
    for user in self.connected_users:
      if user.get_sid() == sid:
        del user 

  def subscribe_to_topic(self, topicId, userId):
    topic = Topic.query.get(topicId)
    if topic:
      topic.subscribe(userId)

  def unsubscribe_from_topic(self, topicId, userId):
    topic = Topic.query.get(topicId)
    topic.unsubscribe(topic)


  def sendToUser(self, sid, data):
    emit('message', data, room=sid)
