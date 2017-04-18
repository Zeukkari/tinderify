# Tinderify
Tinder tool, supports autoswiping users, chatting and storing statistics.

## Installation
1. Install Python dependencies: `pip install flask pynder jsonpickle peewee`
2. Install frontend dependencies: `cd frontend && bower install`
3. Get your facebook access token and id. Run `cd backend && cp config.py.example config.py` and add your facebook auth info to config.py. To find your token and id follow this guide: https://gist.github.com/taseppa/66fc7239c66ef285ecb28b400b556938
4. Start with `python server.py` and open localhost:5000 in web browser.
