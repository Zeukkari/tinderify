import json
import flask
from flask import Flask
import pynder
from flask import request
import db
import sys
import api
import config
import webbrowser
import mock_session
# from mock_session import *
app = Flask(__name__, static_folder='../frontend/app', static_url_path='/')
app.debug=True
session = None

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
    global session
    # print mock_session.x()
    if not isMockingEnabled:
        session = pynder.Session(facebook_token=config.facebook_auth["access_token"], facebook_id=config.facebook_auth["facebook_id"])
    else:
        session = mock_session.MockSession()
    db.connect()
    # if len(sys.argv) > 1 and sys.argv[1] == "--like":
    #     autolike_users(session)

@app.route('/api/autolike')
def autolike_users():
    """
    Swipe right on all users until likes are exhausted
    :return: Total users and matched users
    """
    return api.autolike_users(session)

@app.route("/api/matches")
def matches():
    """
    Get all new matches
    :return: new matches
    """
    return api.matches(session)

@app.route("/api/users")
def get_users():
    """
    Get all new matches
    :return: new matches
    """
    return api.users()

@app.route("/api/message", methods=["POST"])
def send_message():
    """
    Send a message to user
    :return: ok
    """
    data = json.loads(request.data)
    return api.send_message(session, data["id"], data["body"])

@app.route("/api/statistics")
def statistics():
    """
    Get statistics of tinder usage
    :return: statistics
    """
    return api.get_statistics(session)

@app.route("/api/updates", methods=["GET"])
def get_updates():
    """
    Get updates, new matches, messages etc.
    :return: updates
    """
    since = request.args.get("since")
    return api.get_updates(session, since)
if __name__ == "__main__":
    init(True)
    webbrowser.open("http://localhost:5000")
    app.run(threaded=True)
