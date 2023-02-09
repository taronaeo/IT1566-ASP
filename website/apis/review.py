import shelve
import random
import string
import datetime

from .. import DB_REVIEW_LOCATION
from ..models import Review
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('from_uid', type=str, required=True)
parser.add_argument('to_uid', type=str, required=True)
parser.add_argument('rating', type=float, required=True)
parser.add_argument('comments', type=str, required=False)

put_parser = reqparse.RequestParser()
put_parser.add_argument('rating', type=float, required=False)
put_parser.add_argument('comments', type=str, required=False)

class ReviewApiEndpoint(Resource):
  def get(self, review_uid):
    with shelve.open(DB_REVIEW_LOCATION) as db:
      try:
        return db[review_uid].__dict__
      except KeyError:
        return { "code": 404, "message": "Review not found."}, 404

  def post(self):
    args = parser.parse_args()
    review_uid  =  ''.join(random.sample(string.ascii_uppercase, 5))
    created_at = datetime.date.today().strftime("%#d/%#m/%Y")

    with shelve.open(DB_REVIEW_LOCATION) as db:
      try:
        review = Review(
          review_uid,
          args['from_uid'],
          args['to_uid'],
          args['rating'],
          args['comments'],
          created_at
        )

        db[review_uid] = review
        return review.__dict__
      except Exception:
        return { "message": "Something went wrong." }, 500



