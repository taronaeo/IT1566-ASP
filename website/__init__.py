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
DB_CHAT_LOCATION = f"{DB_BASE_LOCATION}_chat"
DB_WALLET_LOCATION = f"{DB_BASE_LOCATION}_wallet"
DB_CAR_LISTING_LOCATION = f"{DB_BASE_LOCATION}_car_listing"
DB_VEHICLE_LOCATION = f"{DB_BASE_LOCATION}_vehicle"
DB_WALLET_TRANSACTION_LOCATION = f"{DB_BASE_LOCATION}_wallet_transaction"
DB_LISTING_TRANSACTION_LOCATION = f"{DB_BASE_LOCATION}_listing_transaction"
DB_REVIEW_LOCATION = f"{DB_BASE_LOCATION}_review_transaction"


DB_PRODUCTS_LOCATION = f"{DB_BASE_LOCATION}_products"


def create_app():
  app = Flask(__name__,
              static_url_path='',
              static_folder='static',
              template_folder='templates')
  api = Api(app)

  # NOTE: To be changed when deploying
  app.config['SECRET_KEY'] = 'abcdefghijklmnopqrstuvwxyz'

  login_manager = LoginManager()
  login_manager.login_view = "auth.login"  # type: ignore
  login_manager.init_app(app)

  from .routes import views, auth, account, vehicle, listing, products, car_listing

  # * BETA WORK
  from .routes import chat

  from .apis.user import UserApiEndpoint
  from .apis.wallet import WalletApiEndpoint
  from .apis.vehicle import VehicleApiEndpoint
  from .apis.listing import ListingApiEndpoint
  from .apis.review import ReviewApiEndpoint
  from .apis.products import ProductApiEndpoint

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  app.register_blueprint(account, url_prefix='/')
  app.register_blueprint(vehicle, url_prefix='/')
  app.register_blueprint(listing, url_prefix='/')
  app.register_blueprint(products, url_prefix='/')
  app.register_blueprint(car_listing, url_prefix='/')

  # * BETA CODE
  app.register_blueprint(chat, url_prefix='/')
  api.add_resource(UserApiEndpoint, "/api/user", "/api/user/<string:uid>")
  api.add_resource(WalletApiEndpoint, "/api/wallet",
                   "/api/wallet/<string:owner_uid>")
  api.add_resource(VehicleApiEndpoint, "/api/vehicle",
                   "/api/vehicle/<string:license_plate>")
  api.add_resource(ListingApiEndpoint, "/api/listing",
                   "/api/listing/<string:uid>")
  api.add_resource(ReviewApiEndpoint, "/api/review",
                   "/api/review/<string:review_uid>")
  api.add_resource(ProductApiEndpoint, "/api/product",
                   "/api/product/<string:product_uid>")

  from .models import User

  @app.errorhandler(404)
  def handleNotFound(error):
    return render_template('/404.html', user=current_user), 404

  @login_manager.user_loader
  def load_user(uid):
    return User.query_uid(uid)

  # * BETA CODE
  @login_manager.unauthorized_handler
  def unauthorised_access():
    flash('Please login to continue')
    next_url = url_for(request.endpoint, **request.view_args)  # type: ignore
    return redirect(url_for('auth.login', next=next_url))

  return app
