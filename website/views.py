"""
  NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  COMMAND TO RUN:
  `py main.py`
"""

import shelve

from . import DB_USER_LOCATION, DB_WALLET_LOCATION, DB_LISTING_LOCATION, DB_VEHICLE_LOCATION
from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template('home.html')

@views.route('/wallet', methods=['GET', 'POST'])
@login_required
def wallet():
  with shelve.open(DB_WALLET_LOCATION) as db:
    wallet = db[current_user.email] # type: ignore

  return render_template("wallet.html", wallet=wallet)

@views.route('/vehicle', methods = ['GET','POST','DELETE'])
@login_required
def vehiclestore():
  with shelve.open(DB_VEHICLE_LOCATION) as db:
    vehicles = []
    for i in db:
      if current_user.email == db[i].owner_uid:
        vehicles.append(db[i])
  return render_template("VehicleStore.html", vehicles = vehicles)

@views.route('/UpdateVehicle',methods = ['GET','POST'])
@login_required
def updatevehicle():
  vehicles = []
  with shelve.open(DB_VEHICLE_LOCATION) as db:
    return render_template("UpdateVehicle.html", owner_uid = current_user.email)

@views.route('/retrieveacc')
@login_required
def retrieveacc():
  with shelve.open(DB_USER_LOCATION) as db:
    return render_template("retrieveacc.html", users=db)

@views.route('/signup')
def signup():
  return render_template("signup.html")

@views.route('/login')
def login():
  return render_template("login.html")

@views.route('/carlistings')
@login_required
def carlistings():
  with shelve.open(DB_LISTING_LOCATION) as db:
    return render_template("car listings.html", owner_uid=current_user.email, cars=db) # type: ignore

@views.route('/contractorlistings')
def contractorlistings():
  return render_template('contractor listings.html')

@views.route('/createcarlistings')
def createcarlistings():
  return render_template('create car listings.html')

@views.route('createcontractorlistings')
def createcontractorlistings():
  return render_template('create contractor listings.html')

@views.route('/updatecarlistings')
def updatecarlistings():
  return render_template('update car listings.html')

@views.route('/updatecontractorlistings')
def updatecontractorlistings():
  return render_template('update contractor listings.html')

@views.route('/UpdateAcc')
def updateA():
  email = request.args.get('email')

  if not email:
    return redirect(url_for('views.retrieveacc'))

  with shelve.open(DB_USER_LOCATION) as db:
    return render_template("UpdateAcc.html", user=db[email])

