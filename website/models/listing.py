from __future__ import annotations

import shelve
import string, random
from .. import DB_LISTING_LOCATION

class Listing():
  def __init__(
    self,
    uid: str, # Randomly generated UID
    owner_uid: str, # User email address
    requirements: str,
    price: float,
    transactions: list
  ):
    self.uid = uid # Randomly generated UID
    self.owner_uid = owner_uid # User email address
    self.requirements = requirements
    self.price = price
    self.transactions = transactions

  @staticmethod
  def create_listing(
    owner_uid: str,
    requirements: str,
    price: float,
  ):
    uid = ''.join(random.sample(string.ascii_uppercase, 5))

    listing = Listing(
      uid,
      owner_uid,
      requirements,
      price,
      []
    )

    with shelve.open(DB_LISTING_LOCATION) as db:
      db[uid] = listing
      db.sync()

    return listing