"""
  !NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  !PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  !COMMAND TO RUN:
  !`py main.py`
"""

import shelve

from .. import DB_LISTING_LOCATION
from flask import Blueprint, render_template
from flask_login import current_user, login_required

listing = Blueprint('listing', __name__)

# ! CAR SECTION
@listing.route('/cars')
def cars():
  with shelve.open(DB_LISTING_LOCATION) as db_listing:
    return render_template('/listing/cars.html', owner_uid=current_user.email, cars=db_listing) # type: ignore

@listing.route('/cars/create')
@login_required
def create_car():
  return render_template('/listing/create_car.html')

@listing.route('/cars/<uid>/update')
@login_required
def update_car(uid: str):
  return render_template('/listing/update_car.html')

# ! CONTRACTOR SECTION
@listing.route('/contractors')
def contractors():
  return render_template('/listing/contractors.html')

@listing.route('/contractors/create')
@login_required
def create_contractor():
  return render_template('/listing/create_contractor.html')

@listing.route('/contractors/<uid>/update')
@login_required
def update_contractor(uid: str):
  return render_template('/listing/update_contractor.html')
