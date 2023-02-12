"""
  ! NOTE TO ALL TEAM MEMBERS: YOU ARE NOT SUPPOSED TO RUN THIS FILE DIRECTLY WITH
  ! PYTHON. PLEASE RUN `main.py` INSTEAD FROM THE PROJECT ROOT FOLDER.

  ! COMMAND TO RUN:
  ! `py main.py`
"""

import shelve
from .. import DB_CHAT_LOCATION

from flask import Blueprint, render_template
from flask_login import current_user

chat = Blueprint('chat', __name__)

@chat.route('/chat')
def view_chat():
  with shelve.open(DB_CHAT_LOCATION) as db_chat:
    return render_template('/account/chat.html',
                            user=current_user,
                            chats=db_chat)
