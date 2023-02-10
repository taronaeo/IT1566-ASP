"""
  * NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  * PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  * COMMAND TO RUN:
  * `py main.py`
"""

from __future__ import annotations

import shelve
from .. import DB_USER_LOCATION
from flask_login import UserMixin

# class BankCard():
#   def __init__(self, number, exp_month, exp_year):
#     self.number = number
#     self.exp_month = exp_month
#     self.exp_year = exp_year

class User(UserMixin):
  def __init__(
    self,
    email,
    full_name,
    phone_number,
    password,
    uid = None,
    access_level = 'User',
    background_check = None,
    training_complete = None,
    ratings = [],
    latest_msg = []
  ):
    super().__init__()
    self.uid = uid or email
    self.access_level = access_level
    self.email = email
    self.full_name = full_name
    self.phone_number = phone_number
    self.password = password
    self.background_check = background_check
    self.training_complete = training_complete
    self.ratings = ratings
    self.latest_msg = latest_msg

  def get_id(self):
    return self.email

  @staticmethod
  def query_user(email: str) -> User | None:
    with shelve.open(DB_USER_LOCATION) as db:
      if email not in db:
        return None

      return db[email]

  def avg_rating(self):
    try:
      ratings = sum(self.ratings) / len(self.ratings)
    except ZeroDivisionError:
      return 0
    return ratings

  @staticmethod
  def update_user(background_check = None, training_complete = None):
    return NotImplemented

  @staticmethod
  def set_latest_msg(uid, last_msg):
    with shelve.open(DB_USER_LOCATION) as db:
      user = db[uid]
      user.latest_msg.append(last_msg)
      if len(user.latest_msg) > 0:
        user.latest_msg.pop(0)
      db[uid] = user
      db.sync()
      return user


  @staticmethod
  def create(
    email,
    full_name,
    phone_number,
    password,
  ) -> User:
    user = User(
      email,
      full_name,
      phone_number,
      password,
    )

    with shelve.open(DB_USER_LOCATION) as db:
      db[email] = user
      db.sync()

    return user