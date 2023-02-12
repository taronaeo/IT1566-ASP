import shelve
import random
import string

from .. import DB_PRODUCTS_LOCATION
from ..models import Product
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('description', type=str, required=True)
parser.add_argument('price', type=float, required=True)

put_parser = reqparse.RequestParser()
put_parser.add_argument('requirements', type=str, required=False)
put_parser.add_argument('price', type=float, required=False)

class ProductApiEndpoint(Resource):
  def get(self, product_uid):
    with shelve.open(DB_PRODUCTS_LOCATION) as db:
      try:
        return db[product_uid].__dict__
      except KeyError:
        return { "code": 404, "message": "Productnot found."}, 404


    

