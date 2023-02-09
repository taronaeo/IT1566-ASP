from website import create_app
from website.sockets import create_socket

from flask_socketio import SocketIO

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 3000

app = create_app()
socketio = create_socket(app)

if __name__ == '__main__':
  # app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)
  socketio.run(app, host=SERVER_HOST, port=SERVER_PORT, debug=True)
