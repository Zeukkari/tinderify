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

        print "%s match=%s %d/%d %f" % (user, match, matches, number_of_users,  float(matches) / number_of_users)
        db.save_user(user, match, [])
        # time.sleep(1) Might be needed
    print("Matched with %d/%d users\n" % (matches, number_of_users))
    return json.dumps({"users": number_of_users, "matched":matches})

def get_conversation(messages):
    conversation = []
    for message in messages:
        conversation.append({"id" : message.id, "message": message.body, "sender": message.sender.name, "sent" : time.mktime(message.sent.timetuple())});

    return sorted(conversation, key=lambda x: x["sent"])

def get_thumbnails(thumbnails):
    return [thumbnail.url for thumbnail in thumbnails]

def get_photos(photos):
    return [photo.url for photo in photos]

def get_matches(session):
    ret = {}
    print("Querying..")
    users = list(db.PotentialMatch.select().where(db.PotentialMatch.matched == True).paginate(1, 100))
    print("Done")
    for user in users:
        print(jsonpickle.dumps(get_thumbnails(user.thumbnails)))
        print(list(user.conversation))
        # print(get_conversation(list(user.conversation)))
        ret[user.tinder_id] = {"name" : user.name, "thumbnails": get_thumbnails(user.thumbnails),
         "photos" : get_photos(user.photos), "messages": get_conversation(list(user.conversation)),
         "id" : user.tinder_id }
        # break

    print ret
    return ret

def update_matches(session):
    return
    matches = session.matches()
    print(matches)
    ret = {}
    for match in matches:
        # print(match)
        # ret[match.id] = {"name": match.user.name, "messages": get_conversation(match.messages),
        # "photos" : match.user.photos, "thumbnails" : match.user.thumbnails, "id" : match.id }
        # print(get_conversation(match.messages))
        db.save_user(match.user, True, match.messages)
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
    match_rate = 0 if number_of_users_swiped == 0 else float(number_of_users_matched)/number_of_users_swiped
    return jsonpickle.dumps({"swiped" : number_of_users_swiped, "matched": number_of_users_matched, "match_rate" : match_rate})
