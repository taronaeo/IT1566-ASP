from __future__ import annotations

import shelve
import string
import random

from .. import DB_CHAT_LOCATION, DB_CONVO_LOCATION
from datetime import datetime

class Conversation():
  def __init__(
    self,
    conversation_uid,
    listing_uid,
    initiator_uid,
    messages
  ):
    self.conversation_uid = conversation_uid
    self.listing_uid = listing_uid
    self.initiator_uid = initiator_uid
    self.messages = messages
  
  @staticmethod
  def create(listing_uid, initiator_uid):
    conversation_uid = '_'.join([listing_uid,initiator_uid])
    conversation = Conversation(
      conversation_uid,
      listing_uid,
      initiator_uid,
      messages=[]
    )
    with shelve.open(DB_CONVO_LOCATION) as db_convo:
      db_convo[conversation_uid] = conversation
    
    return conversation

  @staticmethod
  def send(
    conversation_uid,
    _from,
    _to,
    message
  ):
    message_uid = ''.join(random.sample(string.ascii_uppercase, 5))
    new_message = Message(
        message_uid,
        _from,
        _to,
        message,
        sent_at=datetime.now().strftime("%H:%M"),
      )

    with shelve.open(DB_CONVO_LOCATION) as db_convo:
      db_convo[conversation_uid].messages.append(new_message)
      return new_message

  @staticmethod
  def check_exists(
    conversation_uid
  ):
    with shelve.open(DB_CONVO_LOCATION) as db_convo:
      if conversation_uid not in db_convo:
        return False
      return True


class Message():
  def __init__(
    self,
    message_uid: str,
    _from: str,
    _to: str,
    message: str,
    sent_at: str,
  ) -> None:
    self.message_uid = message_uid
    self._from = _from
    self._to = _to
    self.message = message
    self.sent_at = sent_at

  
