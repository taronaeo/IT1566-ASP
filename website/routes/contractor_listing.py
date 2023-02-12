"""
  ! NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  ! PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  ! COMMAND TO RUN:
  ! `py main.py`
"""

import shelve

from .. import DB_CONTRACTOR_LISTING_LOCATION
from flask import Blueprint, request, render_template
from flask_login import current_user, login_required

contractor_listing = Blueprint('contractor_listing', __name__)


@contractor_listing.route('/contractors')
def contractors():
  query = request.args.get('query', '').strip()

  return render_template('/listing/contractors.html',
                         user=current_user,
                         contractors={})


@contractor_listing.route('/contractors/create')
@login_required
def create_contractor():
  return render_template('/listing/create_contractor.html',
                         user=current_user)


@contractor_listing.route('/contractors/<uid>/update')
@login_required
def update_contractor(uid: str):
  return render_template('/listing/update_contractor.html',
                         user=current_user)
