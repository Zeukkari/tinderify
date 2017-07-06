from peewee import *
from pprint import pprint
import time
import datetime
import jsonpickle

db = SqliteDatabase('tinder.db')

def connect():
    """
    Connect to database and create tables if they don't exist
    :return:
    """
    print("connecting")
    db.connect()
    db.create_tables([PotentialMatch, Photo, Thumbnail, Interest, Conversation], safe=True)

def save_user(user, messages, is_matched=False):
    """
    Save user to database
    :param user: user to save
    :param is_matched: was the user, also saved to database
    :return:
    """
    saved_user = PotentialMatch(tinder_id=user.id, name=user.name, common_connections=len(user.common_connections),
                                connection_count=0, age=user.age, distance=user.distance_km,
                                bio=user.bio, first_shown_date=datetime.datetime.now(), matched=is_matched)
    saved_user.save()

    for photo in user.photos:
        Photo(url=photo, user=saved_user).save()

    for thumbnail in user.thumbnails:
        Thumbnail(url=thumbnail, user=saved_user).save()

    for message in messages:
        Conversation(body=message.body, sent=time.mktime(message.sent.timetuple()), user=saved_user, sender=message.sender).save()

    # This is not yet working
    # for interest in user.common_likes:
    #     print(jsonpickle.dumps(interest))
    #     Interest(name=interest, user=saved_user).save()

def user_exists(tinder_id):
    return PotentialMatch.select().where(PotentialMatch.tinder_id == tinder_id).exists()

def mark_user_matched(tinder_id):
    PotentialMatch.update(matched=True, match_date=datetime.datetime.now()).where(PotentialMatch.tinder_id==tinder_id).execute()

class PotentialMatch(Model):
    tinder_id = CharField()
    name = CharField()
    common_connections = IntegerField()
    connection_count = IntegerField()
    matched = BooleanField(default=False)
    age = IntegerField()
    distance = IntegerField()
    bio = CharField(null=True)
    first_shown_date = DateTimeField()
    match_date = DateTimeField(null=True)

    class Meta:
        database = db  # This model uses the "people.db" database.


class Photo(Model):
    url = CharField()
    user = ForeignKeyField(PotentialMatch, related_name="photos")

    class Meta:
        database = db

class Interest(Model):
    name = CharField()
    user = ForeignKeyField(PotentialMatch, related_name="interests")

    class Meta:
        database = db

class Thumbnail(Model):
    url = CharField()
    user = ForeignKeyField(PotentialMatch, related_name="thumbnails")

    class Meta:
        database = db

class Conversation(Model):
    body = CharField()
    sent = DateTimeField()
    sender = CharField()
    user = ForeignKeyField(PotentialMatch, related_name="conversation")
    # tinder_message_id = CharField()

    class Meta:
        database = db
