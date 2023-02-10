import json
import shelve

from . import DB_CHAT_LOCATION,DB_USER_LOCATION, DB_LISTING_LOCATION,DB_CONVO_LOCATION
from .models.chat import Message, Conversation

from flask import request
from flask_socketio import SocketIO, emit

def create_socket(app):
  socketio = SocketIO(app, cors_allowed_origins='*')


  @socketio.on('receive')
  def handle_connect():
    with shelve.open(DB_CONVO_LOCATION) as db_convo, shelve.open(DB_USER_LOCATION) as db_user:
      for conversation in db_convo.values():
        emit('recv_message', conversation.__dict__,broadcast=True)
    print('New Connection')

  @socketio.on('system')
  def handle_system(data):
    print(f'From SYSTEM events: {data}')

  @socketio.on('conversation')
  def create_convo(data):
    print(f"New conversation: {data}")
    if not Conversation.check_exists(data['conversation_uid']):
      conversation = Conversation.create(data['listing_uid'], data['initiator_uid'])
      

  @socketio.on('message')
  def handle_message(data):
    print(f'New Message: {data}')
    if Conversation.check_exists(data['conversation_uid']):
      Conversation.send(data['conversation_uid'],data['_from'],data['_to'],data['message'])
   
   # message = Message.send(data['listing_uid'], data['_from'], data['_to'], data['message'] )
    #emit('recv_message', message.__dict__, broadcast=True)

  # @socketio.on('channel')
  # def channel(data):
  #   print(f"data:{data}")
    

          

     


  



  return socketio