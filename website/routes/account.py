"""
  ! NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  ! PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  ! COMMAND TO RUN:
  ! `py main.py`
"""

import shelve

from .. import DB_USER_LOCATION, DB_WALLET_LOCATION, DB_CAR_LISTING_LOCATION, DB_REVIEW_LOCATION, DB_PRODUCTS_LOCATION


from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import current_user, login_required
from ..models import Wallet, WalletCard, Listing

account = Blueprint('account', __name__)


@account.route('/account/wallet', methods=['GET', 'POST'])
def wallet():
  with shelve.open(DB_USER_LOCATION) as db_user, shelve.open(DB_WALLET_LOCATION) as db_wallet:
    if request.method == 'POST':
      bank = request.form.get('bank')
      card_number = request.form.get('card_number')
      card_number = card_number.replace(" ", "")
      card_name = request.form.get('card_name')
      cvv = int(request.form.get('cvv'))
      exp_month = str(request.form.get('exp_month'))
      exp_yr = str(request.form.get('exp_yr'))

      exp_date = exp_month + '/' + exp_yr

      WalletCard.create_card(
          current_user.uid,
          bank,
          card_name,
          card_number,
          cvv,
          exp_date
      )
      return redirect(url_for('account.wallet'))
    return render_template('/account/wallet.html', user=current_user, wallet=db_wallet[current_user.uid])


@account.route('/account/wallet/payment/<wallet_uid>/<trans_type>/<amount>', methods=['GET', 'POST'])
def wallet_payment(wallet_uid, trans_type, amount):
  with shelve.open(DB_USER_LOCATION) as db_user, shelve.open(DB_WALLET_LOCATION) as db_wallet:
    if trans_type not in ["topup", "withdraw"]:
      abort(404)
    if not float(amount):
      abort(404)
    if request.method == 'POST':
      bank = request.form.get('bank')
      card_number = request.form.get('card_number')
      card_number = card_number.replace(" ", "")
      card_name = request.form.get('card_name')
      cvv = int(request.form.get('cvv'))
      exp_month = str(request.form.get('exp_month'))
      exp_yr = str(request.form.get('exp_yr'))
      total_amount = request.form.get('total-amount')

      exp_date = exp_month + '/' + exp_yr

      WalletCard.create_card(
          current_user.uid,
          bank,
          card_name,
          card_number,
          cvv,
          exp_date
      )
      return redirect(url_for("account.wallet_payment", wallet_uid=wallet_uid, trans_type=trans_type, amount=total_amount))
    if trans_type == 'topup':
      transaction = "Top Up"
    elif trans_type == 'withdraw':
      transaction = "Withdraw"
    payment_methods = db_wallet[current_user.uid].payment_methods
    return render_template('/account/wallet_payment.html', user=current_user,
                           wallet=db_wallet[current_user.uid],
                           payment_methods=payment_methods,
                           current_payment=payment_methods[0],
                           amount=amount,
                           transaction=transaction)


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
          return render_template('/account/profile.html', user=current_user, wallet=db_wallet[current_user.uid], cars=db_listing, reviews=db_review, db_user=db_user)


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
                                    reviews=db_review,
                                    db_user=db_user))
          if uid not in db_user:
            abort(404)
          return render_template('/account/external_profile.html', user=current_user, wallet=db_wallet[uid], cars=db_listing, reviews=db_review, profile_user=db_user[uid], db_user=db_user)


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


@account.route('/admin/dashboard')
@login_required
def get_dashboard():
  userCount = 0
  listingCount = 0
  productCount = 0
  with shelve.open(DB_USER_LOCATION) as db_user:

    with shelve.open(DB_CAR_LISTING_LOCATION) as db_listing:
      with shelve.open(DB_WALLET_LOCATION) as db_wallet:
        with shelve.open(DB_PRODUCTS_LOCATION) as db_products:
          for user in db_user.values():
            userCount += 1
          for listing in db_listing.values():
            listingCount += 1
          for product in db_products.values():
            productCount += 1
          return render_template('/admin/dashboard.html',
                                 user=current_user,
                                 users=db_user,
                                 userCount=userCount,
                                 listingCount=listingCount,
                                 wallet=db_wallet,
                                 productCount=productCount)


@account.route('/ratingfor/<uid>')
def ratings(uid: str):
  with shelve.open(DB_USER_LOCATION) as db_user:
    return render_template('/account/rate.html', user=current_user, for_uid=uid)
