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

class BankCard():
  def __init__(self, number, exp_month, exp_year):
    self.number = number
    self.exp_month = exp_month
    self.exp_year = exp_year

class User(UserMixin):
  def __init__(
    self,
    email,
    full_name,
    phone_number,
    password,
    uid = None,
    card_information = None,
    bank_information = None,
    background_check = None,
    training_complete = None
  ):
    super().__init__()
    self.uid = uid | email
    self.email = email
    self.full_name = full_name
    self.phone_number = phone_number
    self.password = password
    self.card_information = card_information
    self.bank_information = bank_information
    self.background_check = background_check
    self.training_complete = training_complete

  def get_id(self):
    return self.email

  @staticmethod
  def query_user(email: str) -> User | None:
    with shelve.open(DB_USER_LOCATION) as db:
      if email not in db:
        return None

      return db[email]
  
  @staticmethod
  def update_user(background_check = None, training_complete = None):
    return NotImplemented
  
  @staticmethod
  def create_user(
    email,
    full_name,
    phone_number,
    password,
    card_information,
    bank_information,
  ) -> User:
    user = User(
      email,
      full_name,
      phone_number,
      password,
      card_information,
      bank_information,
    )

    with shelve.open(DB_USER_LOCATION) as db:
      db[email] = user
      db.sync()
    
    return user