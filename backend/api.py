import json
import jsonpickle
from flask import request
import db
import time

def autolike_users(session):
    matches = 0
    number_of_users = 0
    for user in session.nearby_users():
        number_of_users += 1
        match = user.like()
        if match:
            matches += 1

        print "%s match=%s %d/%d %f" % (user, match, matches, number_of_users, float(matches) / number_of_users)
        db.save_user(user, match)
        # time.sleep(1) Might be needed
    print("Matched with %d/%d users\n" % (matches, number_of_users))
    return json.dumps({"users": number_of_users, "matched":matches})

def get_conversation(messages):
    conversation = []
    for message in messages:
        conversation.append({"id" : message.id, "message": message.body, "sender": message.sender.name, "sent" : time.mktime(message.sent.timetuple())});

    return sorted(conversation, key=lambda x: x["sent"])

def users(session):
    ret = {}
    users = list(db.PotentialMatch.select().where(db.PotentialMatch.matched == True).paginate(1, 50))
    for user in users:
        ret[user.id] = {"name" : user.name, "thumbnails": user.thumbnails, "photos" : user.photos }
        # ret.append(str(user.photos).split(","))
    print ret
    return jsonpickle.dumps(ret)

def get_matches(matches):
    ret = {}
    for match in matches:
        ret[match.id] = {"name": match.user.name, "messages": get_conversation(match.messages),
        "photos" : match.user.photos, "thumbnails" : match.user.thumbnails }
    return ret

def matches(session):
    matches = get_matches(session.matches())
    # print matches
    return jsonpickle.dumps(matches)

def send_message(session, id, body):
    ret = session._api.message(id, body)
    return "ok"

def get_updates(session, since):
    ret = session.updates(since)
    print ret
    updates = get_matches(ret)
    return jsonpickle.dumps(updates)

def get_statistics(session):
    number_of_users_swiped = db.PotentialMatch.select().count()
    number_of_users_matched = db.PotentialMatch.select().where(db.PotentialMatch.matched == True).count()
    match_rate = float(number_of_users_matched)/number_of_users_swiped
    return jsonpickle.dumps({"swiped" : number_of_users_swiped, "matched": number_of_users_matched, "match_rate" : match_rate})
