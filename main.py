import json
import functools
import jwt
from datetime import timedelta
from jwt.exceptions import ExpiredSignatureError
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit, disconnect, join_room
from flask_jwt import JWT, jwt_required, current_identity, _jwt
from models import db, User, Topic#, Subscription #, Post,Subscription
from messenger import Messenger

messenger = Messenger()

def authenticate(uname, password):
  user = User.query.filter_by(username=uname).first()
  if user and user.check_password(password):
    return user

def identity(payload):
  return User.query.get(payload['identity'])

def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=7)
  CORS(app)
  db.init_app(app)
  db.create_all(app=app)
  return app

app = create_app()
app.app_context().push()
JWT(app, authenticate, identity)
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

counter = 0

# https://github.com/miguelgrinberg/Flask-SocketIO/issues/568

# def authenticated_only(f):
#     @functools.wraps(f)
#     def wrapped(*args, **kwargs):
#         if not request.json:
#             disconnect()
#         else:
#             return f(*args, **kwargs)
#     return wrapped


'''


@app.route('/getSubscribers/<topicId>')
def get_subs(topicId):
  topic = Topic.query.get(topicId)
  if topic:
    users = topic.get_subscribers()
    return jsonify([ user.toDict() for user in users ])
  return 'topic '+topicId+' not found', 404
'''

@app.route('/')
def client_app():
  return app.send_static_file('index.html')

@jwt_required()
@app.route('/getAuth')
def auth_status():
  return '%s' % current_identity

@app.route('/createUser/<username>/<password>')
def create_user(username, password):
  user = User(username=username)
  user.set_password(password)
  db.session.add(user)
  db.session.commit()
  return username+" saved!"


@app.route('/createpost/<userId>/<topicId>/<text>')
def create_post(userId, topicId, text):
  messenger.new_post(userId, topicId, text)
  return 'post created!'

@app.route('/createTopic/<text>')
def create_topic(text):
  topic = Topic(text=text)
  db.session.add(topic)
  db.session.commit()
  return jsonify({'topicId':topic.id, 'text':topic.text})


@app.route('/topics')
def get_topics():
  topics = Topic.query.all()
  return jsonify([topic.toDict() for topic in topics])

@app.route('/userTopics/<userId>')
def get_user_topics(userId):
  user = User.query.get(userId)
  return jsonify(user.get_topics_json())


@app.route('/feed/<userId>')
def get_feed(userId):
  user = User.query.get(userId)
  if user:
    return jsonify(user.get_feed_json())
  else :
    return 'user not found'


@app.route('/users')
def get_users():
  users = User.query.all()
  return jsonify([ user.toDict() for user in users ])

@app.route('/subscribe/<userId>/<topicId>')
def subscribe_to_topic(userId, topicId):
  messenger.subscribe_to_topic(topicId, userId)
  return 'subscription created '


'''
Sockets
'''

@socketio.on('increment')
def increment(data):
  global counter
  counter += 1
  print('Counter increated to: '+ str(counter) )
  emit('incremented', {'counter': counter}, broadcast=True)

@socketio.on('connect')
def test_connect():
  sid = request.sid
  token = request.args['token']
  print('New client connected')
  try:
    decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    userId = decoded['identity']
    user = User.query.get(userId)
    messenger.add_online_user(user, sid)
    emit('connected', {'counter': counter, 'userId': userId, 'username':user.username})
  except ExpiredSignatureError:
    emit('expired')
  

@socketio.on('disconnect')
def test_disconnect():
  print('Client disconnected')

if __name__ == "__main__":
  socketio.run(app, host='0.0.0.0', port=8080, debug=True)