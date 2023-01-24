"""
  ! NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  ! PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  ! COMMAND TO RUN:
  ! `py main.py`
"""

import shelve
from .. import DB_VEHICLE_LOCATION

from flask import Blueprint, render_template
from flask_login import current_user, login_required

vehicle = Blueprint('vehicle', __name__)

@vehicle.route('/vehicle')
@login_required
def vehicles():
  with shelve.open(DB_VEHICLE_LOCATION) as db:
    vehicles = []
    for i in db:
      if current_user.email == db[i].owner_uid: # type: ignore
        vehicles.append(db[i])
  return render_template("/vehicle/vehicles.html",
                          user=current_user,
                          vehicles=vehicles)

@vehicle.route('/vehicle/<uid>/update')
@login_required
def update_vehicle(uid: str):
  vehicles = []
  with shelve.open(DB_VEHICLE_LOCATION) as db:
    return render_template("/vehicle/update_vehicle.html",
                            user=current_user,
                            owner_uid=current_user.email) # type: ignore
