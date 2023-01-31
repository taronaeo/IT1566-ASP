"""
  ! NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  ! PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  ! COMMAND TO RUN:
  ! `py main.py`
"""

import re
from ..models import User, Wallet

from flask import Blueprint, flash, url_for, request, redirect, render_template
from flask_login import AnonymousUserMixin, current_user, login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login', next=url_for('views.home')))

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if not isinstance(current_user, AnonymousUserMixin):
    return redirect(url_for('views.home'))

  if request.method == 'POST':
    next_url = request.args.get('next')

    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email or password is empty
    if not email or not password:
      flash('Enter an email and password')
      return redirect(url_for('auth.login'))

    user = User.query_user(email)
    if not user:
      flash('Account does not exist')
      return redirect(url_for('auth.login'))

    if user.password == password:
      login_user(user, remember=True)
      return redirect(next_url or url_for('views.home'))

  return render_template('/auth/login.html',
                          user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  if not isinstance(current_user, AnonymousUserMixin):
    return redirect(url_for('views.home'))

  if request.method == 'POST':
    next_url = request.args.get('next')

    full_name = request.form.get('full_name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')

    if not full_name or \
        not phone_number or \
        not email or \
        not password or \
        not password_confirm:
      flash('All fields must not be empty')
      return redirect(url_for('auth.signup'))

    if not re.match(r'^\d{4}\s\d{4}$', phone_number):
      flash('Invalid phone number')
      return redirect(url_for('auth.signup'))

    if not re.match(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
      flash('Invalid email address')
      return redirect(url_for('auth.signup'))

    if password != password_confirm:
      flash('Password and Confirm Password must be the same')
      return redirect(url_for('auth.signup'))

    user = User.create(email, full_name, phone_number, password)
    Wallet.create_wallet(email)
    login_user(user, remember=True)
    return redirect(next_url or url_for('views.home'))

  return render_template('/auth/signup.html',
                          user=current_user)
