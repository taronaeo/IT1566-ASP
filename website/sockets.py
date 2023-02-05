import json
import shelve

from . import DB_CHAT_LOCATION
from .models.chat import Message

from flask_socketio import SocketIO, emit

def create_socket(app):
  socketio = SocketIO(app, cors_allowed_origins='*')

  @socketio.on('connect')
  def handle_connect():
    with shelve.open(DB_CHAT_LOCATION) as db_chat:
      for message in db_chat.values():
        emit('recv_message', message.__dict__)

    print('New Connection')

  @socketio.on('system')
  def handle_system(data):
    print(f'From SYSTEM events: {data}')

  @socketio.on('message')
  def handle_message(data):
    print(f'New Message: {data}')
    message = Message.send(data['listing_uid'], data['user_uid_1'], data['user_uid_2'], data['message'])
    emit('recv_message', message.__dict__, broadcast=True)

  return socketio