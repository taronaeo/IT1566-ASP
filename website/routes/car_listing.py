import re
import shelve

from .. import UPLOAD_DIR, DB_USER_LOCATION, DB_LISTING_LOCATION
from ..utils import check_filename
from ..models import Listing

from flask import Blueprint, abort, flash, url_for, request, redirect, render_template
from flask_login import current_user, login_required

car_listing = Blueprint('car_listing', __name__)


@car_listing.route('/cars')
def cars():
  query = request.args.get('query', '').strip()

  with shelve.open(DB_LISTING_LOCATION) as db_listing:
    listings = db_listing.values()

    if query:
      listings = filter(lambda x: re.search(
        query,
        x.title,
        re.IGNORECASE
      ), db_listing.values())
      listings = list(listings)

    return render_template('/listing/cars.html',
                           user=current_user,
                           cars=listings,
                           query=query)


@car_listing.route('/cars/<uid>')
def view(uid: str):
  with shelve.open(DB_USER_LOCATION) as db_user, \
          shelve.open(DB_LISTING_LOCATION) as db_listing:

    if uid not in db_listing:
      abort(404)

    listing_data = db_listing[uid]
    listing_owner = db_listing[uid].owner_uid

    if listing_owner not in db_user:
      abort(404)

    listing_creator = db_user[listing_owner]

    return render_template('/listing/view_car.html',
                           user=current_user,
                           listings=db_listing,
                           listing_data=listing_data,
                           listing_creator=listing_creator)


@car_listing.route('/cars/create', methods=['GET', 'POST'])
@login_required
def create():
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
      return redirect(url_for('car_listing.create',
                              title=title,
                              vehicle_plate=vehicle_plate,
                              vehicle_location=vehicle_location,
                              requirements=requirements,
                              price=price))

    if not 6 <= len(title) <= 60:
      flash('Title must be within 6 to 60 characters long')
      return redirect(url_for('car_listing.create',
                              title=title,
                              vehicle_plate=vehicle_plate,
                              vehicle_location=vehicle_location,
                              requirements=requirements,
                              price=price))

    if not 4 <= len(vehicle_plate) <= 8:
      flash('Vehicle plate seem to be invalid')
      return redirect(url_for('car_listing.create',
                              title=title,
                              vehicle_plate=vehicle_plate,
                              vehicle_location=vehicle_location,
                              requirements=requirements,
                              price=price))

    if not check_filename(vehicle_img.filename):
      flash('Invalid file type. Only PNG and JPG files are accepted')
      return redirect(url_for('car_listing.create',
                              title=title,
                              vehicle_plate=vehicle_plate,
                              vehicle_location=vehicle_location,
                              requirements=requirements,
                              price=price))

    try:
      price = float(price)
    except ValueError:
      flash('Invalid price. It should be in decimal format')
      return redirect(url_for('car_listing.create',
                              title=title,
                              vehicle_plate=vehicle_plate,
                              vehicle_location=vehicle_location,
                              requirements=requirements,
                              price=price))

    filename = secure_filename(vehicle_img.filename)  # type: ignore
    vehicle_img.save(f'{UPLOAD_DIR}/{filename}')

    Listing.create(
        current_user.uid,  # type: ignore
        title,
        filename,
        vehicle_plate.upper(),
        vehicle_location,
        requirements,
        price
    )
    return redirect(url_for('car_listing.cars'))

  return render_template('/listing/create_car.html',
                         user=current_user)


@car_listing.route('/cars/<uid>/update', methods=['GET', 'POST'])
@login_required
def update(uid: str):
  with shelve.open(DB_LISTING_LOCATION) as db_listing:
    if uid not in db_listing:
      abort(404)

    listing = db_listing[uid]

    if request.method == 'POST':
      title = request.form.get('title', '')
      vehicle_img = request.files.get('vehicle_img')
      vehicle_plate = request.form.get('vehicle_plate', '')
      vehicle_location = request.form.get('vehicle_location', '')
      requirements = request.form.get('requirements', '')
      price = request.form.get('price', '')

      if title and (not 6 <= len(title) <= 60):
        flash('Title must be within 6 to 60 characters long')
        return redirect(url_for('car_listing.create',
                                title=title,
                                vehicle_plate=vehicle_plate,
                                vehicle_location=vehicle_location,
                                requirements=requirements,
                                price=price))
      else:
        listing.title = title

      if vehicle_plate and (not 4 <= len(vehicle_plate) <= 8):
        flash('Vehicle plate seem to be invalid')
        return redirect(url_for('car_listing.create',
                                title=title,
                                vehicle_plate=vehicle_plate,
                                vehicle_location=vehicle_location,
                                requirements=requirements,
                                price=price))
      else:
        listing.vehicle_plate = vehicle_plate

      if vehicle_img and (not check_filename(vehicle_img.filename)):
        flash('Invalid file type. Only PNG and JPG files are accepted')
        return redirect(url_for('car_listing.create',
                                title=title,
                                vehicle_plate=vehicle_plate,
                                vehicle_location=vehicle_location,
                                requirements=requirements,
                                price=price))
      elif vehicle_img:
        filename = secure_filename(vehicle_img.filename)  # type: ignore
        vehicle_img.save(f'{UPLOAD_DIR}/{filename}')
        listing.vehicle_img = filename

      if price:
        try:
          price = float(price)
          listing.price = price
        except ValueError:
          flash('Invalid price. It should be in decimal format')
          return redirect(url_for('car_listing.create',
                                  title=title,
                                  vehicle_plate=vehicle_plate,
                                  vehicle_location=vehicle_location,
                                  requirements=requirements,
                                  price=price))

        db_listing[uid] = listing
        db_listing.sync()

        flash('Update successful')
        return redirect(url_for('car_listing.view', uid=uid))

    return render_template('/listing/update_car.html',
                           user=current_user,
                           listing=db_listing[uid])


@car_listing.route('/cars/<uid>/update/status/<status>')
@login_required
def update_status(uid: str, status: str):
  with shelve.open(DB_LISTING_LOCATION) as db_listing:
    if uid not in db_listing:
      return abort(404)

    if status not in ['LISTED', 'DELISTED', 'ACCEPTED', 'EXPIRED']:
      return abort(404)

    Listing.set_status(uid, status)
    flash(f'Listing {status.lower()}')
    return redirect(url_for('car_listing.view', uid=uid))


@car_listing.route('/cars/<uid>/delete')
def delete(uid: str):
  with shelve.open(DB_LISTING_LOCATION) as db_listing:
    if uid not in db_listing:
      abort(404)

    if current_user.uid != db_listing[uid].owner_uid:  # type: ignore
      flash('Unable to delete listing, unauthorised request')
      abort(404)

    del db_listing[uid]
    flash('Listing successfully deleted')

  return redirect(url_for('car_listing.cars'))
