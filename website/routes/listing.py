"""
  ! NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  ! PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  ! COMMAND TO RUN:
  ! `py main.py`
"""

import shelve

from .. import UPLOAD_DIR, DB_CAR_LISTING_LOCATION, DB_WALLET_LOCATION
from ..models import WalletTransaction

from flask import Blueprint, flash, url_for, request, redirect, render_template
from flask_login import current_user

listing = Blueprint('listing', __name__)

# ! Job Start and end


@listing.route('/cars/<string:uid>/start', methods=['GET', 'POST'])
def jobstart(uid):
  if request.method == 'POST':
    with shelve.open(DB_CAR_LISTING_LOCATION) as db_listing:
      listing = db_listing[uid]

      front_of_vehicle_img = request.files.get('front_of_vehicle_img')
      left_of_vehicle_img = request.files.get('left_of_vehicle_img')
      right_of_vehicle_img = request.files.get('right_of_vehicle_img')
      back_of_vehicle_img = request.files.get('back_of_vehicle_img')

      interior1_img = request.files.get('interior1_img')
      interior2_img = request.files.get('interior2_img')
      interior3_img = request.files.get('interior3_img')
      interior4_img = request.files.get('interior4_img')

      if not front_of_vehicle_img or \
              not left_of_vehicle_img or \
              not right_of_vehicle_img or \
              not back_of_vehicle_img:
        flash('All exterior photos are required')
        return redirect(url_for('listing.jobstart', uid=uid))

      front_of_vehicle_img.save(f'{UPLOAD_DIR}/{uid}_front_of_vehicle_bf.jpg')
      left_of_vehicle_img.save(f'{UPLOAD_DIR}/{uid}_left_of_vehicle_bf.jpg')
      right_of_vehicle_img.save(f'{UPLOAD_DIR}/{uid}_right_of_vehicle_bf.jpg')
      back_of_vehicle_img.save(f'{UPLOAD_DIR}/{uid}_back_of_vehicle_bf.jpg')

      listing.exterior_photos.append(f'{uid}_front_of_vehicle_bf.jpg')
      listing.exterior_photos.append(f'{uid}_left_of_vehicle_bf.jpg')
      listing.exterior_photos.append(f'{uid}_right_of_vehicle_bf.jpg')
      listing.exterior_photos.append(f'{uid}_back_of_vehicle_bf.jpg')

      if interior1_img:
        interior1_img.save(f'{UPLOAD_DIR}/{uid}_interior1.jpg')
        listing.interior_photos.append(f'{uid}_interior1.jpg')

      if interior2_img:
        interior2_img.save(f'{UPLOAD_DIR}/{uid}_interior2.jpg')
        listing.interior_photos.append(f'{uid}_interior2.jpg')

      if interior3_img:
        interior3_img.save(f'{UPLOAD_DIR}/{uid}_interior3.jpg')
        listing.interior_photos.append(f'{uid}_interior3.jpg')

      if interior4_img:
        interior4_img.save(f'{UPLOAD_DIR}/{uid}_interior4.jpg')
        listing.interior_photos.append(f'{uid}_interior4.jpg')

      listing.status = 'STARTED'
      db_listing[uid] = listing
      flash('Successfully started job')
      return redirect(url_for('listing.jobend', uid=uid))

  return render_template('/job/jobstart.html', user=current_user)


@listing.route('/cars/<string:uid>/end', methods=['GET', 'POST'])
def jobend(uid):
  if request.method == 'POST':
    with shelve.open(DB_CAR_LISTING_LOCATION) as db_listing, \
      shelve.open(DB_WALLET_LOCATION) as db_wallet:
      listing = db_listing[uid]
      contractor_wallet = db_wallet[current_user.uid]
      listing_owner_wallet = db_wallet[listing.owner_uid]

      front_of_vehicle_img = request.files.get('front_of_vehicle_img')
      left_of_vehicle_img = request.files.get('left_of_vehicle_img')
      right_of_vehicle_img = request.files.get('right_of_vehicle_img')
      back_of_vehicle_img = request.files.get('back_of_vehicle_img')

      interior1_img = request.files.get('interior1_img')
      interior2_img = request.files.get('interior2_img')
      interior3_img = request.files.get('interior3_img')
      interior4_img = request.files.get('interior4_img')

      if not front_of_vehicle_img or \
              not left_of_vehicle_img or \
              not right_of_vehicle_img or \
              not back_of_vehicle_img:
        flash('All exterior photos are required')
        return redirect(url_for('listing.jobstart', uid=uid))

      front_of_vehicle_img.save(f'{UPLOAD_DIR}/{uid}_front_of_vehicle_af.jpg')
      left_of_vehicle_img.save(f'{UPLOAD_DIR}/{uid}_left_of_vehicle_af.jpg')
      right_of_vehicle_img.save(f'{UPLOAD_DIR}/{uid}_right_of_vehicle_af.jpg')
      back_of_vehicle_img.save(f'{UPLOAD_DIR}/{uid}_back_of_vehicle_af.jpg')

      listing.exterior_photos.append(f'{uid}_front_of_vehicle_af.jpg')
      listing.exterior_photos.append(f'{uid}_left_of_vehicle_af.jpg')
      listing.exterior_photos.append(f'{uid}_right_of_vehicle_af.jpg')
      listing.exterior_photos.append(f'{uid}_back_of_vehicle_af.jpg')

      if interior1_img:
        interior1_img.save(f'{UPLOAD_DIR}/{uid}_interior1.jpg')
        listing.interior_photos.append(f'{uid}_interior1.jpg')

      if interior2_img:
        interior2_img.save(f'{UPLOAD_DIR}/{uid}_interior2.jpg')
        listing.interior_photos.append(f'{uid}_interior2.jpg')

      if interior3_img:
        interior3_img.save(f'{UPLOAD_DIR}/{uid}_interior3.jpg')
        listing.interior_photos.append(f'{uid}_interior3.jpg')

      if interior4_img:
        interior4_img.save(f'{UPLOAD_DIR}/{uid}_interior4.jpg')
        listing.interior_photos.append(f'{uid}_interior4.jpg')

      contractor_wallet.balance += listing.price
      WalletTransaction.create_transaction(
        current_user.uid,
        'topup',
        listing.price,
        f'Job Completion {listing.uid}'
      )

      listing_owner_wallet.balance -= listing.price
      WalletTransaction.create_transaction(
        listing.owner_uid,
        'withdraw',
        listing.price,
        f'Listing Completion {listing.uid}'
      )

      listing.status = 'COMPLETED'
      db_wallet[current_user.uid] = contractor_wallet
      db_wallet[listing.owner_uid] = listing_owner_wallet
      db_listing[uid] = listing

      flash('Successfully ended job')
      return redirect(url_for('car_listing.cars'))

  return render_template('/job/jobend.html', user=current_user)
