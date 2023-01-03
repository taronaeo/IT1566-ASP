import shelve

from .. import DB_USER_LOCATION
from ..models import User
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required=True)
parser.add_argument('password', type=str, required=True)
parser.add_argument('password_confirm', type=str, required=True)
parser.add_argument('full_name', type=str, required=True)
parser.add_argument('home_address', type=str, required=True)
parser.add_argument('phone_number', type=str, required=True)

class UserApiEndpoint(Resource):
  def get(self, uid):
    with shelve.open(DB_USER_LOCATION) as db:
      try:
        return db[uid].__dict__
      except KeyError:
        return { "code": 404, "message": "User not found." }, 404

  def post(self):
    args = parser.parse_args()

    with shelve.open(DB_USER_LOCATION) as db:
      try:
        exists = db[args['email']]
        if exists:
          return { "message": "Account already exists." }, 409

        if args['password'] != args['password_confirm']:
          return {"message": "Passwords do not match."}

        user = User(
          args['email'],
          args['password'],
          args['full_name'],
          args['home_address'],
          args['phone_number'],
          vehicles=[],
          uid=args['email'],
        )

        db[args['email']] = user
        return user.__dict__
      except Exception:
        return { "message": "Something went wrong." }, 500