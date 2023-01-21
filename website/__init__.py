"""
  NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  COMMAND TO RUN:
  `py main.py`
"""

import shelve
from flask import Flask
from flask_restful import Api
from flask_login import LoginManager

DB_BASE_LOCATION = "instance/sgdetailmart"
DB_USER_LOCATION = f"{DB_BASE_LOCATION}_user"
DB_WALLET_LOCATION = f"{DB_BASE_LOCATION}_wallet"
DB_LISTING_LOCATION = f"{DB_BASE_LOCATION}_listing"
DB_VEHICLE_LOCATION = f"{DB_BASE_LOCATION}_vehicle"
DB_WALLET_TRANSACTION_LOCATION = f"{DB_BASE_LOCATION}_wallet_transaction"
DB_LISTING_TRANSACTION_LOCATION = f"{DB_BASE_LOCATION}_listing_transaction"

def create_app():
  app = Flask(__name__,
              static_url_path='',
              static_folder='static',
              template_folder='templates')
  api = Api(app)

  app.config['SECRET_KEY'] = 'abcdefghijklmnopqrstuvwxyz' # NOTE: To be changed when deploying

  login_manager = LoginManager()
  login_manager.login_view = "auth.login"
  login_manager.init_app(app)

  from .auth import auth
  from .views import views
  from .apis.user import UserApiEndpoint
  from .apis.wallet import WalletApiEndpoint
  from .apis.vehicle import VehicleApiEndpoint
  from .apis.listing import ListingApiEndpoint

  app.register_blueprint(auth, url_prefix='/')
  app.register_blueprint(views, url_prefix='/')
  api.add_resource(UserApiEndpoint, "/api/user", "/api/user/<string:uid>")
  api.add_resource(WalletApiEndpoint, "/api/wallet", "/api/wallet/<string:owner_uid>")
  api.add_resource(VehicleApiEndpoint, "/api/vehicle", "/api/vehicle/<string:license_plate>")
  api.add_resource(ListingApiEndpoint, "/api/listing", "/api/listing/<string:uid>")

  @login_manager.user_loader
  def load_user(email):
    with shelve.open(DB_USER_LOCATION) as db:
      try:
        return db[email]
      except KeyError:
        pass
  
  return app
