from __future__ import annotations

import shelve
import string, random

from datetime import datetime
from .. import DB_PRODUCTS_LOCATION

class Product():
  def __init__(
    self,
    uid: str, # Randomly generated UID
    name: str, # Product Name
    product_img: str,
    description: str,
    price: float,
    category: str,
  ):
    self.uid = uid # Randomly generated UID
    self.name = name
    self.product_img = product_img
    self.description = description
    self.price = price
    self.category = category


  @staticmethod
  def create(
    name: str,
    product_img: str,
    description: str,
    price: float,
    category: str
  ):
    uid = ''.join(random.sample(string.ascii_uppercase, 5))

    product = Product(
      uid,
      name,
      product_img,
      description,
      price,
      category
    )
    with shelve.open(DB_PRODUCTS_LOCATION) as db_product:
      db_product[uid] = product
      db_product.sync()

    return product