import json
import jsonpickle
from flask import request
import db
import time
import pynder
from threading import Thread


class TinderAPI:
    session = None
    last_update = None
    websocket_connection = None

    def __init__(self, access_token, facebook_id, websocket_connection):
        self.session = pynder.Session(facebook_token=access_token, facebook_id=facebook_id)
        self.websocket_connection = websocket_connection
        print access_token, facebook_id
        print(self.session)
        Thread(target=self.update_matches).start()
        # self.update_matches()

    def autolike_users(self):
        matches = 0
        number_of_users = 0
        for user in session.nearby_users():
            db.save_user(user, [])
            number_of_users += 1
            match = user.like()
            if match:
                matches += 1

            print "%s match=%s %d/%d %f" % (user, match, matches, number_of_users,  float(matches) / number_of_users)
            db.mark_as_matched(user, match, [])
            # time.sleep(1) Might be needed
        print("Matched with %d/%d users\n" % (matches, number_of_users))
        return json.dumps({"users": number_of_users, "matched": matches})

    def get_conversation(self, messages):
        conversation = []
        for message in messages:
            conversation.append({"id": message.id, "message": message.body,
                                 "sender": message.sender.name, "sent": time.mktime(message.sent.timetuple())});

        return sorted(conversation, key=lambda x: x["sent"])

    def get_thumbnails(self, thumbnails):
        return [thumbnail.url for thumbnail in thumbnails]

    def get_photos(self, photos):
        return [photo.url for photo in photos]

    def get_conversation_db(self, conversations):
        return [{"id": message.id, "message": message.body, "sender": message.sender, "sent": message.sent} for message in conversations]

    def get_matches(self):
        ret = {}
        users = list(db.PotentialMatch.select().where(
            db.PotentialMatch.matched == True).paginate(1, 100))

        for user in users:
            # print(jsonpickle.dumps(get_thumbnails(user.thumbnails)))
            # print(list(user.conversation))
            # print(get_conversation(list(user.conversation)))
            ret[user.tinder_id] = {"name": user.name, "thumbnails": self.get_thumbnails(user.thumbnails),
                                   "photos": self.get_photos(user.photos), "messages": self.get_conversation_db(user.conversation),
                                   "id": user.tinder_id}

        print ret
        return ret


    def pynder_user_to_object(self, user):
        return {"name": user.name, "photos" : list(user.photos), "thumbnails" : list(user.thumbnails), "id" : user.id }

    def update_matches(self):
        matches = self.session.matches()
        print(matches)
        ret = {}
        for match in matches:
            # print(match)
            if db.user_exists(match.user.id):
                db.mark_user_matched(match.user.id)
            else:
                db.save_user(match.user, match.messages, True)

        for n in range(10):
            self.websocket_connection.emit('updates', ret)
            time.sleep(1)
            print("sending")
        return ret

    def matches(self):
        # matches = get_matches(session.matches())

        matches = self.get_matches()

        # print matches
        return jsonpickle.dumps(matches)

    def judge_recommendations(self, user_id, like):
        if like:
            ret = self.session._api.like(user_id)
            print(ret)
            return jsonpickle.dumps(ret)
        else:
            print("disliking")
            return jsonpickle.dumps(self.session._api.dislike(user_id))

    def get_recommendations(self):
        ret = []
        recommendations = self.session.nearby_users()

        for counter, recommendation in enumerate(recommendations):
            db.save_user(recommendation, [])
            print(recommendation)
            ret.append(self.pynder_user_to_object(recommendation))
            if counter == 10:
                break

        return jsonpickle.dumps(ret)

    def send_message(self, id, body):
        ret = self.session._api.message(id, body)
        return "ok"

    def get_updates(self, since):
        ret = self.session.updates(since)
        print ret
        updates = get_matches(ret)
        return jsonpickle.dumps(updates)

    def get_statistics(self):
        number_of_users_swiped = db.PotentialMatch.select().count()
        number_of_users_matched = db.PotentialMatch.select().where(
            db.PotentialMatch.matched == True).count()
        match_rate = 0 if number_of_users_swiped == 0 else float(
            number_of_users_matched) / number_of_users_swiped
        return jsonpickle.dumps({"swiped": number_of_users_swiped, "matched": number_of_users_matched, "match_rate": match_rate})
