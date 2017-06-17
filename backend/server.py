import json
import flask
from flask import Flask
from flask import request
from flask import Response
import db
import sys
import api
import config
import webbrowser
import mock_session

from flask import Flask, render_template
from flask_socketio import SocketIO

# from mock_session import *
app = Flask(__name__, static_folder='../frontend/app', static_url_path='/')
app.debug=True
tinder = None
socketio = SocketIO(app)

@app.route('/bower_components/<path:filename>')
def serve_static(filename):
    return flask.send_from_directory('../frontend/bower_components', filename)

@app.route('/<path:filename>')
def test(filename):
    return flask.send_from_directory('../frontend/app', filename)

@app.route('/')
def root():
    return app.send_static_file('index.html')

def init(isMockingEnabled):
    db.connect()

    global tinder
    if not isMockingEnabled:
        tinder = api.TinderAPI(config.facebook_auth["access_token"], config.facebook_auth["facebook_id"], socketio)
    else:
        tinder = mock_session.MockSession()

    print "here"

@app.route("/api/matches")
def matches():
    """
    Get all new matches
    :return: new matches
    """
    return Response(tinder.matches(), "application/json")

@app.route("/api/matches/<user_id>/message", methods=["POST"])
def send_message():
    """
    Send a message to user
    :return: ok
    """
    data = json.loads(request.data)
    return tinder.send_message(user_id, data["body"])

@app.route("/api/commands/statistics")
def statistics():
    """
    Get statistics of tinder usage
    :return: statistics
    """
    return tinder.get_statistics()

@app.route('/api/commands/autolike')
def autolike_users():
    """
    Swipe right on all users until likes are exhausted
    :return: Total users and matched users
    """
    return tinder.autolike_users()

if __name__ == "__main__":
    init(config.misc.get("isMockingEnabled", False))
    if not app.debug:
         webbrowser.open("http://localhost:5000")
    # app.run(threaded=True)
    socketio.run(app)
