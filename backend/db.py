from peewee import *
from pprint import pprint

db = SqliteDatabase('tinder.db')

def connect():
    """
    Connect to database and create tables if they don't exist
    :return:
    """
    db.connect()
    db.create_tables([PotentialMatch, Photo, Thumbnail, Interest], safe=True)

def save_user(user, is_matched):
    """
    Save user to database
    :param user: user to save
    :param is_matched: was the user, also saved to database
    :return:
    """
    saved_user = PotentialMatch(tinder_id=user.id, name=user.name, common_connections=len(user.common_connections),
                                connection_count=0, age=user.age, distance=user.distance_km, matched=is_matched)
    saved_user.save()

    for photo in user.photos:
        Photo(url=photo, user=saved_user).save()

    for thumbnail in user.thumbnails:
        Thumbnail(url=thumbnail, user=saved_user).save()

        # for interest in user.common_interests:
        #     Interest(name=interest, user=saved_user).save()


class PotentialMatch(Model):
    tinder_id = CharField()
    name = CharField()
    common_connections = IntegerField()
    connection_count = IntegerField()
    matched = BooleanField()
    age = IntegerField()
    distance = IntegerField()

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
