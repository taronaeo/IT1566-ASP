"""
  * NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  * PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  * COMMAND TO RUN:
  * `py main.py`
"""

from __future__ import annotations

import shelve
import string
import random

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
    uid: str,
    email: str,
    full_name: str,
    phone_number: str,
    password: str,
    access_level: str = 'User',
    background_check: bool = False,
    training_complete: bool = False,
    ratings: list = []
  ):
    super().__init__()
    self.uid = uid
    self.access_level = access_level
    self.email = email
    self.full_name = full_name
    self.phone_number = phone_number
    self.password = password
    self.background_check = background_check
    self.training_complete = training_complete
    self.ratings = ratings

  def get_id(self):
    return self.uid

  def avg_rating(self):
    try:
      ratings = sum(self.ratings) / len(self.ratings)
    except ZeroDivisionError:
      return 5
    return ratings

  @staticmethod
  def query_uid(uid: str) -> User | None:
    with shelve.open(DB_USER_LOCATION) as db_user:
      if uid not in db_user:
        return None

      return db_user[uid]

  @staticmethod
  def query_email(email: str) -> User | None:
    with shelve.open(DB_USER_LOCATION) as db_user:
      users = list(filter(lambda user: user.email == email, db_user.values()))
      user = users[0] if len(users) > 0 else None

      return user

  @staticmethod
  def update_user(background_check=None, training_complete=None):
    return NotImplemented

  @staticmethod
  def create(
    email: str,
    full_name: str,
    phone_number: str,
    password: str,
  ) -> User:
    uid = ''.join(random.sample(string.ascii_uppercase, 5))

    user = User(
      uid,
      email,
      full_name,
      phone_number,
      password,
    )

    with shelve.open(DB_USER_LOCATION) as db:
      db[uid] = user
      db.sync()

    return user
