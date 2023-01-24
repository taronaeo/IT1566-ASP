from __future__ import annotations

import shelve
import string, random

from datetime import datetime
from .. import DB_LISTING_LOCATION

class Listing():
  def __init__(
    self,
    uid: str, # Randomly generated UID
    owner_uid: str, # User email address
    vehicle_img: str,
    vehicle_make: str,
    vehicle_model: str,
    vehicle_plate: str,
    vehicle_location: str,
    requirements: str,
    price: float,
    transactions: list,
    created_at
  ):
    self.uid = uid # Randomly generated UID
    self.owner_uid = owner_uid # User email address
    self.vehicle_img = vehicle_img
    self.vehicle_make = vehicle_make
    self.vehicle_model = vehicle_model
    self.vehicle_plate = vehicle_plate
    self.vehicle_location = vehicle_location
    self.requirements = requirements
    self.price = price
    self.transactions = transactions
    self.created_at = created_at

  @staticmethod
  def create_listing(
    owner_uid: str,
    vehicle_img: str,
    vehicle_make: str,
    vehicle_model: str,
    vehicle_plate: str,
    vehicle_location: str,
    requirements: str,
    price: float,
  ):
    uid = ''.join(random.sample(string.ascii_uppercase, 5))

    listing = Listing(
      uid,
      owner_uid,
      vehicle_img,
      vehicle_make,
      vehicle_model,
      vehicle_plate,
      vehicle_location,
      requirements,
      price,
      [],
      datetime.now().timestamp()
    )

    with shelve.open(DB_LISTING_LOCATION) as db:
      db[uid] = listing
      db.sync()

    return listing