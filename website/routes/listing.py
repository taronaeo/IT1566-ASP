"""
  ! NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  ! PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  ! COMMAND TO RUN:
  ! `py main.py`
"""

from .. import UPLOAD_DIR
from ..utils import check_filename

from werkzeug.utils import secure_filename
from flask import Blueprint, flash, request, redirect, render_template
from flask_login import current_user

listing = Blueprint('listing', __name__)

# ! Job Start and end


@listing.route('/job/jobstart')
def jobstart():
  if request.method == 'POST':
    vehicle_img = request.files.get('vehicle_img')

    if not vehicle_img:
      flash('All fields must not be empty')
      return redirect(request.url)

    if not check_filename(vehicle_img.filename):
      flash('Invalid file type. Only PNG and JPG files are accepted')
      return redirect(request.url)

    filename = secure_filename(vehicle_img.filename)  # type: ignore
    vehicle_img.save(f'{UPLOAD_DIR}/{filename}')

  return render_template('/job/jobstart.html', user=current_user)


@listing.route('/job/jobend')
def jobend():
  if request.method == 'POST':
    vehicle_img = request.files.get('vehicle_img')

    if not vehicle_img:

      flash('All fields must not be empty')
      return redirect(request.url)

    if not check_filename(vehicle_img.filename):
      flash('Invalid file type. Only PNG and JPG files are accepted')
      return redirect(request.url)

    filename = secure_filename(vehicle_img.filename)  # type: ignore
    vehicle_img.save(f'{UPLOAD_DIR}/{filename}')

  return render_template('/job/jobend.html', user=current_user)
