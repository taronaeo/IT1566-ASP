"""
  NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  COMMAND TO RUN:
  `py main.py`
"""

import os
from flask import Flask, flash, url_for, request, redirect, render_template
from flask_login import LoginManager, current_user
from flask_restful import Api

UPLOAD_DIR = os.path.join(os.getcwd(), 'website', 'static', 'uploads')

DB_BASE_LOCATION = "instance/sgdetailmart"
DB_USER_LOCATION = f"{DB_BASE_LOCATION}_user"
DB_WALLET_LOCATION = f"{DB_BASE_LOCATION}_wallet"
DB_LISTING_LOCATION = f"{DB_BASE_LOCATION}_listing"
DB_VEHICLE_LOCATION = f"{DB_BASE_LOCATION}_vehicle"
DB_WALLET_TRANSACTION_LOCATION = f"{DB_BASE_LOCATION}_wallet_transaction"
DB_LISTING_TRANSACTION_LOCATION = f"{DB_BASE_LOCATION}_listing_transaction"
DB_REVIEW_LOCATION = f"{DB_BASE_LOCATION}_review_transaction"

def create_app():
  app = Flask(__name__,
              static_url_path='',
              static_folder='static',
              template_folder='templates')
  api = Api(app)

  app.config['SECRET_KEY'] = 'abcdefghijklmnopqrstuvwxyz' # NOTE: To be changed when deploying

  login_manager = LoginManager()
  login_manager.login_view = "auth.login" # type: ignore
  login_manager.init_app(app)

  from .routes import views, auth, account, vehicle, listing

  from .apis.user import UserApiEndpoint
  from .apis.wallet import WalletApiEndpoint
  from .apis.vehicle import VehicleApiEndpoint
  from .apis.listing import ListingApiEndpoint
  from .apis.review import ReviewApiEndpoint

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  app.register_blueprint(account, url_prefix='/')
  app.register_blueprint(vehicle, url_prefix='/')
  app.register_blueprint(listing, url_prefix='/')
  api.add_resource(UserApiEndpoint, "/api/user", "/api/user/<string:uid>")
  api.add_resource(WalletApiEndpoint, "/api/wallet", "/api/wallet/<string:owner_uid>")
  api.add_resource(VehicleApiEndpoint, "/api/vehicle", "/api/vehicle/<string:license_plate>")
  api.add_resource(ListingApiEndpoint, "/api/listing", "/api/listing/<string:uid>")
  api.add_resource(ReviewApiEndpoint, "/api/review", "/api/review/<string:review_uid>")

  from .models import User

  @app.errorhandler(404)
  def handleNotFound(error):
    return render_template('/404.html', user=current_user), 404

  @login_manager.user_loader
  def load_user(email):
    return User.query_user(email)

  # * BETA CODE
  @login_manager.unauthorized_handler
  def unauthorised_access():
    flash('Please login to continue')
    next_url = url_for(request.endpoint, **request.view_args) # type: ignore
    return redirect(url_for('auth.login', next=next_url))

  return app
