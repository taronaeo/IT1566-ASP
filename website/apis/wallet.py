import shelve
import datetime

from .. import DB_WALLET_LOCATION
from ..models import Wallet, WalletTransaction
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('owner_uid', type=str, required = True)
parser.add_argument('balance', type=float, required = False)
parser.add_argument('stamps_collected', type=int, required = False)
parser.add_argument('transactions', type=str, required = False)

put_parser = reqparse.RequestParser()
put_parser.add_argument('type', type=str, required=True)
put_parser.add_argument('amount', type=float, required=True)

class WalletApiEndpoint(Resource):
  def get(self, owner_uid):
    with shelve.open(DB_WALLET_LOCATION) as db:
      try:
        return db[owner_uid].to_json()
      except KeyError:
        return { "message": "Wallet not found." }, 404

  def post(self):
    args = parser.parse_args()

    with shelve.open(DB_WALLET_LOCATION) as db:
      try:
        if args['owner_uid'] in db:
          return { "message": "Wallet already exists." }, 409

        wallet = Wallet(args['owner_uid'], 0, 0, [])
        db[args['owner_uid']] = wallet
        return wallet.to_json()
      except Exception:
        return { "message": "Something went wrong." }, 500

  def put(self, owner_uid):
    args = put_parser.parse_args()
    timestamp = datetime.datetime.now().strftime('%d/%m/%Y %I:%M %p')

    with shelve.open(DB_WALLET_LOCATION) as db:
      if owner_uid not in db:
        return { "code": 404, "message": "Wallet not found." }, 404

      wallet = db[owner_uid]
      if args['type'] == 'increment':
        wallet.balance += args['amount']
        transaction = WalletTransaction('topup', args['amount'], '-', timestamp)
        wallet.transactions.append(transaction)
      else:
        wallet.balance -= args['amount']
        transaction = WalletTransaction('withdraw', args['amount'], '-', timestamp)
        wallet.transactions.append(transaction)

      db[owner_uid] = wallet
      return wallet.to_json()

  def delete(self,owner_uid):
    with shelve.open(DB_WALLET_LOCATION) as db:
      try:
        del db[owner_uid]
        return {'code': 200, 'message': 'Wallet Deleted'}, 200
      except KeyError:
        return {'code': 404, 'message': 'Wallet not found'}, 404
      except Exception:
        return {'code': 500, 'message': 'Somthing went wrong'}, 500
