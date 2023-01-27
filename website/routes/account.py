"""
  ! NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  ! PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  ! COMMAND TO RUN:
  ! `py main.py`
"""

import shelve
from .. import DB_USER_LOCATION, DB_WALLET_LOCATION

from flask import Blueprint, render_template
from flask_login import current_user, login_required

account = Blueprint('account', __name__)

@account.route('/wallet')
@login_required
def get_wallet():
  with shelve.open(DB_WALLET_LOCATION) as wallet_db:
    wallet = db[current_user.email] # type: ignore

  return render_template('/account/wallet.html',
                          user=current_user,
                          wallet=wallet)

@account.route('/account')
@login_required
def get_account():
  with shelve.open(DB_USER_LOCATION) as db_user:
    return render_template('/account/account.html',
                            user=current_user,
                            users=db_user)

@account.route('/account/update')
@login_required
def update_account():
  with shelve.open(DB_USER_LOCATION) as db_user:
    return render_template('/account/update_account.html',
                            user=db_user[current_user.email])

@account.route('/account/admin-dashboard')
def dashboard():
  with shelve.open(DB_USER_LOCATION) as db_user:
    return render_template('/Admin/Dashboard.html', user=db_user.)
