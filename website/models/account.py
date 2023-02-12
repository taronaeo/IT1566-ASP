"""
  ! NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  ! PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  ! COMMAND TO RUN:
  ! `py main.py`
"""

import shelve
from .. import DB_USER_LOCATION, DB_WALLET_LOCATION, DB_CAR_LISTING_LOCATION, DB_REVIEW_LOCATION

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

account = Blueprint('account', __name__)


@account.route('/account/wallet')
def wallet():
  with shelve.open(DB_USER_LOCATION) as db_user, shelve.open(DB_WALLET_LOCATION) as db_wallet:
    return render_template('/account/wallet.html', user=current_user, wallet=db_wallet[current_user.uid])


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
                           user=current_user)


@account.route('/account/profile')
def profile():
  with shelve.open(DB_USER_LOCATION) as db_user:
    with shelve.open(DB_WALLET_LOCATION) as db_wallet:
      with shelve.open(DB_CAR_LISTING_LOCATION) as db_listing:
        with shelve.open(DB_REVIEW_LOCATION) as db_review:
          return render_template('/account/profile.html', user=current_user, wallet=db_wallet[current_user.uid], cars=db_listing, reviews=db_review)


@account.route('/account/profile/<string:uid>')
def other_profile(uid):
  with shelve.open(DB_USER_LOCATION) as db_user:
    with shelve.open(DB_WALLET_LOCATION) as db_wallet:
      with shelve.open(DB_CAR_LISTING_LOCATION) as db_listing:
        with shelve.open(DB_REVIEW_LOCATION) as db_review:
          if uid == current_user.uid:  # type: ignore
            return redirect(url_for('account.profile',
                                    user=current_user,
                                    wallet=db_wallet[uid],
                                    cars=db_listing,
                                    reviews=db_review))
          return render_template('/account/external_profile.html', user=db_user[uid], wallet=db_wallet[uid], cars=db_listing, reviews=db_review)


@account.route('/account/inbox')
@login_required
def get_inbox():
  with shelve.open(DB_USER_LOCATION) as db_user:
    with shelve.open(DB_WALLET_LOCATION) as db_wallet:
      return render_template('/account/wallet.html', user=current_user, wallet=db_wallet[current_user.uid])


@account.route('/review')
def review():
  with shelve.open(DB_USER_LOCATION) as db_user:
    with shelve.open(DB_REVIEW_LOCATION) as db_review:
      return render_template('/account/review.html', user=current_user, reviews=db_review)
