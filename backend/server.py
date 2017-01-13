import json
import flask
from flask import Flask
import pynder
from flask import request
import db
import sys
import api

app = Flask(__name__, static_folder='../frontend/app', static_url_path='/')
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

def main():
    facebook_auth_token = open("token.cfg").read()
    global session
    session = pynder.Session(facebook_auth_token)
    db.connect()
    # if len(sys.argv) > 1 and sys.argv[1] == "--like":
    #     autolike_users(session)

@app.route('/autolike')
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

# @app.route("/api/updates", methods=["GET"])
# def get_updates():

if __name__ == "__main__":
    main()
    print sys.argv
    app.run()