import shelve

from .. import DB_VEHICLE_LOCATION
from ..models import Vehicle

from datetime import datetime
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('license_plate', type=str, required=True)
parser.add_argument('owner_uid', type=str, required=True)
parser.add_argument('vehicle_make', type=str, required=True)
parser.add_argument('vehicle_model', type=str, required=True)
parser.add_argument('unlock_system_installed', type=bool, required=True)

update_parser = reqparse.RequestParser()
update_parser.add_argument('type',type = str, required = True)
update_parser.add_argument('vehicle_make',type = str, required = True)
update_parser.add_argument('vehicle_model',type = str, required = True)
update_parser.add_argument('uid',type = str, required = True)
class VehicleApiEndpoint(Resource):
  def get(self, license_plate):
    with shelve.open(DB_VEHICLE_LOCATION) as db:
      try:
        return db[license_plate].__dict__
      except KeyError:
        return { "code": 404, "message": "Vehicle not found." }, 404

  def post(self):
    args = parser.parse_args()

    with shelve.open(DB_VEHICLE_LOCATION) as db:
      try:
        if args['license_plate'] in db:
          return { "message": "Vehicle already exists." }, 409
  
        vehicle = Vehicle(
          args['license_plate'],
          args['owner_uid'],
          args['vehicle_make'],
          args['vehicle_model'],
          args['unlock_system_installed'],
          created_at=datetime.timestamp(datetime.now())
        )

        db[args['license_plate']] = vehicle
        return vehicle.__dict__
      except Exception:
        return { "message": "Something went wrong." }, 500
        
  def put(self,license_plate):
    args = update_parser.parse_args()
    with shelve.open(DB_VEHICLE_LOCATION) as db:
      try:
        if license_plate not in db:
          return {'code': 404, "message": "Vehicle does not exist." }, 404
        if args['type'] == 'update':
          vehicle = Vehicle(
            args['uid'],
            db[license_plate].owner_uid,
            args['vehicle_make'],
            args['vehicle_model'],
            db[license_plate].unlock_system_installed,
            created_at=db[license_plate].created_at
          )
          db[args['uid']] = vehicle
          if license_plate != args['uid']:
            del db[license_plate]
          return vehicle.__dict__
      except KeyError:
        return {'code': 404, 'message': 'Vehicle not found'}, 404
      except Exception:
        return {"code": 500, "message": "Something went wrong."}, 500

  def delete(self,license_plate):
    with shelve.open(DB_VEHICLE_LOCATION) as db:
      try:
        del db[license_plate]
        return {'code': 200, 'message': 'Vehicle Deleted'}, 200
      except KeyError:
        return {'code': 404, 'message': 'Vehicle not found'}, 404
      except Exception: 
        return {'code': 500, 'message': 'Somthing went wrong'}, 500
