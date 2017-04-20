import datetime

class MockSession:

    def matches(self):
        print "Getting matches"
        user_data = User(name="testuser", id=1, connections= 56, age=35, distance=35)
        self.matches = [Match(user_data)]
        return self.matches

    def updates(self, since=None):
        self.matches[0].messages.append(Message(5, "yo", "dick", datetime.datetime.now()))
        return self.matches

class User:
    def __init__(self, id, name, connections, age, distance):
        self.name = name
        self.connections = connections
        self.common_connections = []
        self.age = age
        self.distance_km = distance
        self.thumbnails = []
        self.photos = []
        self.id = id

class Match:
    def __init__(self, user):
        self.user = user
        self.id = user.id
        self.messages = [Message(5, "hello", "dick", datetime.datetime.now())]

class Message:
    def __init__(self, id, text, name, sent):
        self.id = id
        self.body = text
        self.sender = User(id=1, name=name,  connections= 56, age=35, distance=35)
        self.sent = sent

        # conversation.append({"id" : message.id, "message": message.body, "sender": message.sender.name, "sent" : time.mktime(message.sent.timetuple())});
