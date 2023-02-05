from __future__ import annotations

import shelve
import string
import random

from .. import DB_CHAT_LOCATION
from datetime import datetime

class Message():
  def __init__(
    self,
    message_uid: str,
    listing_uid: str,
    _from: str,
    _to: str,
    message: str,
    sent_at: float
  ) -> None:
    self.message_uid = message_uid
    self.listing_uid = listing_uid
    self._from = _from
    self._to = _to
    self.message = message
    self.sent_at = sent_at

  @staticmethod
  def send(
    listing_uid: str,
    _from: str,
    _to: str,
    message: str,
  ):
    message_uid = ''.join(random.sample(string.ascii_uppercase, 5))

    new_message = Message(
      message_uid,
      listing_uid,
      _from,
      _to,
      message,
      sent_at=datetime.now().timestamp()
    )

    with shelve.open(DB_CHAT_LOCATION) as db_chat:
      db_chat[message_uid] = new_message

    return new_message
