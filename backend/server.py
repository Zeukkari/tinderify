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
import access_token

from flask import Flask, render_template
from flask_socketio import SocketIO

from flask_cors import CORS, cross_origin
from threading import Thread
import atexit
app = Flask(__name__, static_folder='./dist', static_url_path='/')

CORS(app)

tinder = None
socketio = SocketIO(app)

@app.route('/<path:filename>')
def serve_file(filename):
    return flask.send_from_directory('./dist', filename)

@app.route('/')
def root():
    f = app.send_static_file('index.html')
    return f

@app.before_first_request
def init():
    db.connect()

    global tinder
    if not config.misc.get("isMockingEnabled", False):
        token = access_token.get_access_token(config.facebook_auth["email"], config.facebook_auth["password"])
        print token
        tinder = api.TinderAPI(token, config.facebook_auth["facebook_id"], socketio)
    else:
        tinder = mock_session.MockSession()

@app.route("/api/users/matches")
def matches():
    """
    Get existing matches
    :return: new matches
    """
    return Response(tinder.matches(), "application/json")

@app.route("/api/users/recommendations")
def recommendations():
    """
    Get a list of recommendations for swiping
    :return: new matches
    """
    return Response(tinder.get_recommendations(), "application/json")

@app.route("/api/users/recommendations/<user_id>/judge", methods=["POST"])
def judge_recommendation(user_id):
    """
    Get a list of recommendations for swiping
    :return: new matches
    """
    data = json.loads(request.data)
    return Response(tinder.judge_recommendations(user_id, data['like']), "application/json")

@app.route("/api/users/matches/<user_id>/message", methods=["POST"])
def send_message(user_id):
    """
    Send a message to user
    :return: ok
    """
    data = json.loads(request.data)
    return Response(tinder.send_message(user_id, data["body"]), "application/json")

@app.route("/api/commands/statistics")
def statistics():
    """
    Get statistics of tinder usage
    :return: statistics
    """
    return Response(tinder.get_statistics(), "application/json")

@app.route('/api/commands/autolike')
def autolike_users():
    """
    Swipe right on all users until likes are exhausted
    :return: Total users and matched users
    """
    return Response(tinder.autolike_users(), "application/json")

# if __name__ == "__main__":
#     # init(config.misc.get("isMockingEnabled", False))
#     # socketio.run(app)
