"""
  ! NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  ! PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  ! COMMAND TO RUN:
  ! `py main.py`
"""

import shelve
from .. import UPLOAD_DIR, DB_LISTING_LOCATION
from ..models import Listing
from ..utils import check_filename

from werkzeug.utils import secure_filename
from flask import Blueprint, flash, url_for, request, redirect, render_template
from flask_login import current_user, login_required

listing = Blueprint('listing', __name__)

# ! CAR SECTION
@listing.route('/cars')
def cars():
  with shelve.open(DB_LISTING_LOCATION) as db_listing:
    return render_template('/listing/cars.html',
                            user=current_user,
                            cars=db_listing)

@listing.route('/cars/create', methods=['GET', 'POST'])
@login_required
def create_car():
  if request.method == 'POST':
    title = request.form.get('title')
    vehicle_img = request.files.get('vehicle_img')
    vehicle_plate = request.form.get('vehicle_plate')
    vehicle_location = request.form.get('vehicle_location')
    requirements = request.form.get('requirements')
    price = request.form.get('price')

    if not title or \
        not vehicle_img or \
        not vehicle_plate or \
        not vehicle_location or \
        not requirements or \
        not price:
      flash('All fields must not be empty')
      return redirect(request.url)

    if not 6 <= len(title) <= 30:
      flash('Title must be within 6 to 30 characters long')
      return redirect(request.url)

    if not 4 <= len(vehicle_plate) <= 8:
      flash('Vehicle plate seem to be invalid')
      return redirect(request.url)

    if not check_filename(vehicle_img.filename):
      flash('Invalid file type. Only PNG and JPG files are accepted')
      return redirect(request.url)

    try:
      price = float(price)
    except ValueError:
      flash('Invalid price. It should be in decimal format')
      return redirect(request.url)

    filename = secure_filename(vehicle_img.filename) # type: ignore
    vehicle_img.save(f'{UPLOAD_DIR}/{filename}')

    Listing.create_listing(current_user.email, title, filename, vehicle_plate.upper(), vehicle_location, requirements, price) # type: ignore
    return redirect(url_for('listing.cars'))

  return render_template('/listing/create_car.html',
                          user=current_user)

@listing.route('/cars/<uid>/update')
@login_required
def update_car(uid: str):
  return render_template('/listing/update_car.html',
                          user=current_user)

# ! CONTRACTOR SECTION
@listing.route('/contractors')
def contractors():
  return render_template('/listing/contractors.html',
                          user=current_user,
                          contractors={})

@listing.route('/contractors/create')
@login_required
def create_contractor():
  return render_template('/listing/create_contractor.html',
                          user=current_user)

@listing.route('/contractors/<uid>/update')
@login_required
def update_contractor(uid: str):
  return render_template('/listing/update_contractor.html',
                          user=current_user)
