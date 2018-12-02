import datetime
import json
import time
from threading import Thread

import dateutil.tz
import jsonpickle
import pynder

import db


class TinderAPI:
    session = None
    last_update = None
    websocket_connection = None

    def __init__(self, access_token, facebook_id, websocket_connection):
        """
        Init function, this starts a new thread which periodically checks for new matches
        :param access_token: Tinder access token
        :param facebook_id: Facebook id
        :param websocket_connection: Websocket connection
        """
        self.session = pynder.Session(facebook_token=access_token, facebook_id=facebook_id)
        self.websocket_connection = websocket_connection
        Thread(target=self.update_matches).start()

    def update_matches(self):
        """
        Check periodically for new matches. Any new matches are communicated to the browser using websocket
        :return:
        """

        while True:
            matches = list(self.session.matches(self.last_update))

            if len(matches) == 0:
                time.sleep(1)  # Check periodically once per second
                continue

            db.save_matches(matches, self.last_update == None)
            self.last_update = datetime.datetime.now(dateutil.tz.tzlocal()).isoformat()
            self.websocket_connection.emit('updates', self.get_matches())
            time.sleep(1)

    def autolike_users(self, max_count):
        """
        Start autoliking tinder users
        :param max_count: maximum number of users to like
        :return: summary of how many users were liked and matched in json
        """
        matches = 0
        number_of_users = 0
        for user in self.session.nearby_users(max_count):
            db.save_user(user, [])
            db.update_user_first_shown_date(user.id)
            number_of_users += 1
            match = user.like()
            db.update_user_swipe_date(user.id, True)
            if match:
                matches += 1

            print "%s match=%s %d/%d %f" % (user, match, matches, number_of_users,  float(matches) / number_of_users)
            time.sleep(0.2) # To prevent spamming the server with too many requests
        print("Matched with %d/%d users\n" % (matches, number_of_users))
        return json.dumps({"users": number_of_users, "matched": matches})

    def get_matches_from_db(self):
        """
        Get matches in the database
        :return: Matches in the database as a dictionary
        """
        ret = {}
        users = list(db.PotentialMatch.select().paginate(1, 10000)) # todo remove hardcoded pagination
        print ("Getting matches")
        for user in users:
            ret[user.tinder_id] = self.database_user_to_object(user)

        return ret

    def matches(self):
        """
        Get matches from DB as a JSON
        :return: matches from DB as a JSON
        """
        matches = self.get_matches_from_db()
        return jsonpickle.dumps(matches)

    def judge_recommendations(self, user_id, like):
        """
        Like or dislike an user
        :param user_id: User to like/dislike
        :param like: To like or not to like
        :return: Result of match as json
        """
        db.update_user_swipe_date(user_id, like)
        if like:
            ret = self.session._api.like(user_id)
            print(ret)
            return jsonpickle.dumps(ret)
        else:
            print("disliking")
            return jsonpickle.dumps(self.session._api.dislike(user_id))

    def get_recommendations(self):
        """
        Get new recommendations from tinder
        :return: Recommendations as JSON
        """
        ret = []
        recommendations = self.session.nearby_users()

        for counter, recommendation in enumerate(recommendations):
            user = db.save_user(recommendation, [])
            db.update_user_first_shown_date(recommendation.id)
            print(recommendation)
            ret.append(self.database_user_to_object(user))
            if counter == 30:
                break

        return jsonpickle.dumps(ret)

    def send_message(self, id, body):
        """
        Send a message to a tinder user
        :param id: user id
        :param body: message content
        :return: "ok"
        """
        print "Sending message"
        print id, body
        ret = self.session._api.message(id, body)
        return "ok"  # todo

    def get_statistics(self):
        """
        Get swiping statistics from database
        :return: swiping statistics as JSON
        """
        number_of_users_swiped = db.PotentialMatch.select().count()
        number_of_users_matched = db.PotentialMatch.select().where(
            db.PotentialMatch.matched == True).count()
        match_rate = 0 if number_of_users_swiped == 0 else float(
            number_of_users_matched) / number_of_users_swiped
        return jsonpickle.dumps({"swiped": number_of_users_swiped, "matched": number_of_users_matched, "match_rate": match_rate})
