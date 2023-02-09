from __future__ import annotations

import shelve
import string, random

from datetime import datetime
from .. import DB_REVIEW_LOCATION

class Review():
  def __init__(
    self,
    review_uid: str,
    from_uid: str,
    to_uid:str,
    rating: float,
    comments: str,
    created_at: str
  ):
    self.review_uid = review_uid
    self.from_uid = from_uid
    self.to_uid = to_uid
    self.rating = rating
    self.comments = comments
    self.created_at = created_at

  @staticmethod
  def create_review(
    from_uid: str,
    to_uid: str,
    rating: float,
    comments:str,
    created_at: str
  ): 
    review_uid  =  ''.join(random.sample(string.ascii_uppercase, 5))

    review = Review(
    review_uid,
    from_uid,
    to_uid,
    rating,
    comments,
    created_at
    )

    with shelve.open(DB_REVIEW_LOCATION) as db:
      db[review_uid] = review
      db.sync()

    return review