# import sys
# sys.path.append('C:\\Users\\linsen\\Documents\\WatchTogether')
from flask_backend.app import socketio, app
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer

# import logging
# logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    #
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()
    #
    socketio.run(app, host='0.0.0.0', debug=True)

    # http_server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    # http_server.serve_forever()
