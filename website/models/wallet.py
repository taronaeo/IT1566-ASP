from __future__ import annotations

import shelve
from .. import DB_WALLET_LOCATION
from datetime import datetime

class Wallet():
  def __init__(
    self,
    uid: str, # User Email Address
    balance: float,
    transactions: list,
  ):
    self.uid = uid
    self.balance = balance
    self.transactions = transactions

  @staticmethod
  def create_wallet(uid: str) -> Wallet:
    wallet = Wallet(uid, 0, [])

    with shelve.open(DB_WALLET_LOCATION) as db:
      db[uid] = wallet
      db.sync()

    return wallet

class WalletTransaction():
  def __init__(
    self,
    transaction_type: str,
    transaction_amount: float,
    transaction_remarks: str,
    transaction_timestamp: float,
  ):
    self.transaction_type = transaction_type
    self.transaction_amount = transaction_amount
    self.transaction_remarks = transaction_remarks
    self.transaction_timestamp = transaction_timestamp

  @staticmethod
  def create_transaction(
    wallet_uid: str,
    transaction_type: str,
    transaction_amount: float,
    transaction_remarks: str
  ):
    transaction = WalletTransaction(
      transaction_type,
      transaction_amount,
      transaction_remarks,
      transaction_timestamp=datetime.now().timestamp()
    )

    with shelve.open(DB_WALLET_LOCATION) as db:
      wallet: Wallet = db[wallet_uid]
      wallet.transactions.append(transaction)
      db[wallet_uid] = wallet
      db.sync()

    return transaction