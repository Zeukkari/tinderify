# Tinderify

[![Build Status](https://travis-ci.org/taseppa/tinderify.svg?branch=master)](https://travis-ci.org/taseppa/tinderify)

Alternative Tinder client/tool, supports autoswiping users, chatting and storing statistics.

## Prerequisites

You need to login at least once using the official Tinder client, brand new users can't be created.

## Installation and running
1. Install Python dependencies: `pip install flask pynder jsonpickle peewee flask-socketio flask-cors`
2. Run `cd backend && cp config.py.example config.py` and add your facebook auth info to config.py. 
3. Start with `FLASK_APP=server.py flask run` and open localhost:5000 in web browser.

## Development

For development setup both frontend and backend support auto-reloading on file changes. 

1. Follow step1 & 2 of the above section
2. Start backend with `FLASK_APP=server.py FLASK_DEBUG=true flask run`
3. Install frontend dependencies `npm install && bower install`
4. Start serving frontend `grunt serve`


