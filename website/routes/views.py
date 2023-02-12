"""
  ! NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  ! PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  ! COMMAND TO RUN:
  ! `py main.py`
"""

from flask import Blueprint, render_template
import shelve
from flask_login import current_user
from .. import DB_PRODUCTS_LOCATION,DB_CAR_LISTING_LOCATION

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
  with shelve.open(DB_PRODUCTS_LOCATION) as db_products, shelve.open(DB_CAR_LISTING_LOCATION) as db_listings:
    return render_template('home.html', user=current_user,db_products=db_products,db_listings=db_listings)



