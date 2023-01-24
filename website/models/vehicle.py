from __future__ import annotations
from datetime import datetime

class Vehicle():
  def __init__(
    self,
    uid, # Vehicle License Plate
    owner_uid, # User Email Address
    vehicle_make,
    vehicle_model,
    unlock_system_installed,
    created_at,
  ):
    self.uid = uid # Vehicle License Plate
    self.owner_uid = owner_uid # User Email Address
    self.vehicle_make = vehicle_make
    self.vehicle_model = vehicle_model
    self.unlock_system_installed = unlock_system_installed
    self.created_at = created_at

  @staticmethod
  def create_vehicle(
    uid,
    owner_uid,
    vehicle_make,
    vehicle_model
  ) -> Vehicle:
    vehicle = Vehicle(
      uid,
      owner_uid,
      vehicle_make,
      vehicle_model,
      unlock_system_installed=False,
      created_at=datetime.now().timestamp()
    )

    return vehicle