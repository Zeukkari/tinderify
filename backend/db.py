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

def save_user(user, messages, is_matched=False, match_id=None):
    """
    Save user to database
    :param user: user to save
    :param is_matched: was the user, also saved to database
    :return:
    """;

    database_user = None

    try:

        database_user = PotentialMatch.get(PotentialMatch.tinder_id == user.id)
        database_user.update( name=user.name, common_connections=len(user.common_connections),
                                connection_count=0, age=user.age, distance=user.distance_km,
                                bio=user.bio, matched=is_matched, match_id=match_id).where(PotentialMatch.tinder_id == user.id).execute()
        print("Updating existing user")

    except DoesNotExist:
        print("Adding new user")
        print(user.id)
        database_user = PotentialMatch.create(tinder_id=user.id, name=user.name, common_connections=len(user.common_connections),
                                connection_count=0, age=user.age, distance=user.distance_km,
                                bio=user.bio, matched=is_matched, match_id=match_id)

        # TODO: These should be updated for existing user
        for photo in user.photos:
            Photo(url=photo, user=database_user).save()

        for thumbnail in user.thumbnails:
            Thumbnail(url=thumbnail, user=database_user).save()

    return database_user

    for message in messages:
        if not Conversation.select().where(Conversation.message_id == message.id).exists():
            Conversation(message_id=message.id, body=message.body, sent=time.mktime(message.sent.timetuple()), user=database_user, sender=message.sender).save()

    # This is not yet working
    # for interest in user.common_likes:
    #     print(jsonpickle.dumps(interest))
    #     Interest(name=interest, user=database_user).save()

def get_user(tinder_id):
    user = PotentialMatch.get(PotentialMatch.tinder_id == user.id)
    return user

def update_user_first_shown_date(tinder_id):
    PotentialMatch.update(first_shown_date=datetime.datetime.now()).where(PotentialMatch.tinder_id==tinder_id).execute()

def update_user_swipe_date(tinder_id, liked):
    PotentialMatch.update(swipe_date=datetime.datetime.now(), liked=liked).where(PotentialMatch.tinder_id==tinder_id).execute()

def user_exists(tinder_id):
    return PotentialMatch.select().where(PotentialMatch.tinder_id == tinder_id).exists()

def mark_user_matched(tinder_id):
    PotentialMatch.update(matched=True, match_date=datetime.datetime.now()).where(PotentialMatch.tinder_id==tinder_id).execute()

class PotentialMatch(Model):
    tinder_id = CharField(unique=True)
    match_id = CharField(unique=True, null=True)
    name = CharField()
    common_connections = IntegerField()
    connection_count = IntegerField()
    matched = BooleanField(default=False)
    age = IntegerField()
    distance = IntegerField()
    bio = CharField(null=True)
    liked = BooleanField(null=True)
    first_shown_date = DateTimeField(null=True)
    swipe_date = DateTimeField(null=True)
    match_date = DateTimeField(null=True)

    class Meta:
        database = db  # This model uses the "people.db" database.


class Photo(Model):
    url = CharField(unique=True)
    user = ForeignKeyField(PotentialMatch, related_name="photos")

    class Meta:
        database = db

class Interest(Model):
    name = CharField()
    user = ForeignKeyField(PotentialMatch, related_name="interests")

    class Meta:
        database = db

class Thumbnail(Model):
    url = CharField(unique=True)
    user = ForeignKeyField(PotentialMatch, related_name="thumbnails")

    class Meta:
        database = db

class Conversation(Model):
    message_id = CharField(null=True) # Tinder internal message id
    body = CharField()
    sent = DateTimeField()
    sender = CharField()
    user = ForeignKeyField(PotentialMatch, related_name="conversation")
    # tinder_message_id = CharField()

    class Meta:
        database = db
