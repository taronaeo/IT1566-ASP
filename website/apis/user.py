import shelve

from .. import DB_USER_LOCATION
from ..models import User
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required=True)
parser.add_argument('password', type=str, required=True)
parser.add_argument('password_confirm', type=str, required=True)
parser.add_argument('full_name', type=str, required=True)
parser.add_argument('phone_number', type=str, required=True)
parser.add_argument('vehicles', type=list, required=False)
parser.add_argument('bank_information', type=str, required=False)
parser.add_argument('training_complete', type=bool, required=False)
parser.add_argument('background_check', type=bool, required=False)

put_parser = reqparse.RequestParser()
put_parser.add_argument('full_name', type=str, required=False)
put_parser.add_argument('phone_number', type=str, required=False)
put_parser.add_argument('password', type=str, required = False)

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
        if args['email'] in db:
          return { "message": "Account already exists." }, 409

        if args['password'] != args['password_confirm']:
          return {"message": "Passwords do not match."}

        user = User(
          args['email'],
          args['password'],
          args['full_name'],
          args['phone_number'],
          uid = args['email'],
          bank_information=args['bank_information'],
          training_complete=args['training_complete'],
          background_check=args['background_check'],
        )

        db[args['email']] = user
        return user.__dict__
      except Exception:
        return { "message": "Something went wrong." }, 500

  def put(self, uid):
    args = put_parser.parse_args()

    with shelve.open(DB_USER_LOCATION) as db:
      if uid not in db:
        return {'code': 404, "message": "Account does not exist." }, 404

      user = db[uid]
      user.full_name = args['full_name'] or user.full_name
      user.phone_number = args['phone_number'] or user.phone_number
      user.password = args['password'] or user.password
      db[uid] = user
      return user.__dict__

  def delete(self, uid):
    with shelve.open(DB_USER_LOCATION) as db:
      try:
        del db[uid]
        return {'code': 200, 'message': 'User Account Deleted'}, 200
      except KeyError:
        return {'code': 404, 'message': 'User Account not found'}, 404
      except Exception: 
        return {'code': 500, 'message': 'Somthing went wrong'}, 500
