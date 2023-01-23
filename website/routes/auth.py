"""
  ! NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  ! PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  ! COMMAND TO RUN:
  ! `py main.py`
"""

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
      return redirect(url_for('account.get_account'))

  return render_template('/auth/login.html',
                          user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  if not isinstance(current_user, AnonymousUserMixin):
    return redirect(url_for('views.home'))

  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    full_name = request.form.get('full_name')
    home_address = request.form.get('home_address')
    phone_number = request.form.get('phone_number')

    if not email or \
      not password or \
      not password_confirm or \
      not full_name or \
      not home_address or \
      not phone_number:
      flash('All fields must not be empty')
      return redirect(url_for('auth.signup'))
    
    if password != password_confirm:
      flash('Password and Confirm Password must be the same')
      return redirect(url_for('auth.signup'))
    
    user = User.create_user(email, password, full_name, home_address, phone_number)
    Wallet.create_wallet(email)
    login_user(user, remember=True)
    return redirect(url_for('account.get_account'))

  return render_template('/auth/signup.html',
                          user=current_user)
