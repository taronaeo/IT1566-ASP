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
    payment_methods: list,
  ):
    self.uid = uid
    self.balance = balance
    self.transactions = transactions
    self.payment_methods = payment_methods
  
  @staticmethod
  def create_wallet(email: str) -> Wallet:
    wallet = Wallet(email, 0, [],[])

    with shelve.open(DB_WALLET_LOCATION) as db:
      db[uid] = wallet
      db.sync()

    return wallet

  @staticmethod
  def del_card(
    wallet_uid: str,
    card:dict,
  ):
    with shelve.open(DB_WALLET_LOCATION) as db:
      wallet = db[wallet_uid]
      index = wallet.payment_methods.index(card)
      del wallet.payment_methods[index]
      db[wallet_uid] = wallet
      db.sync()
    return wallet

  
class WalletTransaction():
  def __init__(
    self,
    transaction_type: str,
    transaction_amount: float,
    transaction_remarks: str,
    transaction_timestamp: str,
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

class WalletCard():
  def __init__(
    self,
    bank:str, #visa, mc
    card_name:str,
    card_number:str,
    cvv: int,
    expiry_date:str,

  ):
    self.bank = bank 
    self.card_name = card_name
    self.card_number = card_number
    self.cvv = cvv
    self.expiry_date = expiry_date

  @staticmethod
  def create_card(
    wallet_uid: str,
    bank:str,
    card_name: str,
    card_number: str,
    cvv: int,
    expiry_date: str
  ):
    card = WalletCard(
      bank,
      card_name,
      card_number,
      cvv,
      expiry_date
    )

    with shelve.open(DB_WALLET_LOCATION) as db:
      wallet: Wallet = db[wallet_uid]
      wallet.payment_methods.append(card.__dict__)
      db[wallet_uid] = wallet
      db.sync()

    return card