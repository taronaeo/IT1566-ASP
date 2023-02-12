from __future__ import annotations

import shelve
import string
import random

from .. import DB_CAR_LISTING_LOCATION
from datetime import datetime


class Listing():
  def __init__(
    self,
    uid: str,  # Randomly generated UID
    status: str,
    owner_uid: str,  # User email address
    title: str,
    vehicle_img: str,
    vehicle_plate: str,
    vehicle_location: str,
    requirements: str,
    price: float,
    accepted_by: str,
    exterior_photos: list,
    interior_photos: list,
    created_at: float,
  ):
    self.uid = uid  # Randomly generated UID
    self.status = status
    self.owner_uid = owner_uid  # User email address
    self.title = title
    self.vehicle_img = vehicle_img
    self.vehicle_plate = vehicle_plate
    self.vehicle_location = vehicle_location
    self.requirements = requirements
    self.price = price
    self.accepted_by = accepted_by
    self.exterior_photos = exterior_photos
    self.interior_photos = interior_photos
    self.created_at = created_at

  @staticmethod
  def create(
    owner_uid: str,
    title: str,
    vehicle_img: str,
    vehicle_plate: str,
    vehicle_location: str,
    requirements: str,
    price: float,
    accepted_by: str,
    exterior_photos: list,
    interior_photos: list,
  ):
    uid = ''.join(random.sample(string.ascii_uppercase, 5))

    listing = Listing(
      uid,
      "LISTED",
      owner_uid,
      title,
      vehicle_img,
      vehicle_plate,
      vehicle_location,
      requirements,
      price,
      accepted_by,
      exterior_photos,
      interior_photos,
      datetime.now().timestamp(),
    )

    with shelve.open(DB_CAR_LISTING_LOCATION) as db_listing:
      db_listing[uid] = listing
      db_listing.sync()

    return listing

  @staticmethod
  def set_status(uid: str, status: str):
    with shelve.open(DB_CAR_LISTING_LOCATION) as db_listing:
      if uid not in db_listing:
        return None

      listing = db_listing[uid]
      listing.status = status

      db_listing[uid] = listing
      db_listing.sync()

    return listing
