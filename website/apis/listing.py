import shelve
import random
import string

from .. import DB_CAR_LISTING_LOCATION
from ..models import Listing
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('owner_uid', type=str, required=True)
parser.add_argument('requirements', type=str, required=True)
parser.add_argument('price', type=float, required=True)

put_parser = reqparse.RequestParser()
put_parser.add_argument('requirements', type=str, required=False)
put_parser.add_argument('price', type=float, required=False)


class ListingApiEndpoint(Resource):
  def get(self, uid):
    with shelve.open(DB_CAR_LISTING_LOCATION) as db:
      try:
        return db[uid].__dict__
      except KeyError:
        return {"code": 404, "message": "Listing not found."}, 404

  def post(self):
    args = parser.parse_args()
    uid = ''.join(random.sample(string.ascii_uppercase, 5))

    with shelve.open(DB_CAR_LISTING_LOCATION) as db:
      try:
        listing = Listing(
          uid,
          args['owner_uid'],
          args['title'],
          args['requirements'],
          args['price'],
          [],
        )

        db[uid] = listing
        return listing.__dict__
      except Exception:
        return {"message": "Something went wrong."}, 500

  def put(self, uid):
    args = put_parser.parse_args()

    with shelve.open(DB_CAR_LISTING_LOCATION) as db:
      if uid not in db:
        return {"code": 404, "message": "Listing does not exist."}, 404

      listing = db[uid]
      listing.requirements = args['requirements'] or listing.requirements
      listing.price = args['price'] or listing.price

      db[uid] = listing
      return listing.__dict__

  def delete(self, uid):
    with shelve.open(DB_CAR_LISTING_LOCATION) as db:
      try:
        del db[uid]
        return {'code': 200, 'message': 'Listing Deleted'}, 200
      except KeyError:
        return {'code': 404, 'message': 'Listing not found'}, 404
      except Exception:
        return {'code': 500, 'message': 'Somthing went wrong'}, 500
