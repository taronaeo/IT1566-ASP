"""
  ! NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  ! PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  ! COMMAND TO RUN:
  ! `py main.py`
"""

from flask import Blueprint, render_template
from flask_login import current_user

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
  return render_template('home.html', user=current_user)



