# Tinderify

[![Build Status](https://travis-ci.org/taseppa/tinderify.svg?branch=master)](https://travis-ci.org/taseppa/tinderify)

Alternative Tinder client/tool, supports autoswiping users, chatting and storing statistics.

## Prerequisites

You need to login at least once using the official Tinder client, brand new users can't be created.

## Installation and running
1. Install lxml: `sudo apt-get install python-lxml` (or what is appropriate for your OS)
2. Install Python dependencies: `pip install flask jsonpickle peewee flask-socketio flask-cors robobrowser`
3. Run `cd backend && cp config.py.example config.py` and add your facebook auth info to config.py. 
4. Start with `./run.sh` and open localhost:5000 in web browser.

## Development

For development setup both frontend and backend support auto-reloading on file changes. 

1. Follow step1 & 2 of the above section
2. Start backend with `./debug.sh`
3. Install frontend dependencies `npm install && bower install`
4. Start serving frontend `grunt serve`

## Todo
* Safer handling of facebook credentials
* Prettier UI
* More statistics
