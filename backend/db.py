from peewee import *
from pprint import pprint

db = SqliteDatabase('tinder.db')

def connect():
    db.connect()
    db.create_tables([PotentialMatch, Photo, Thumbnail, Interest], safe=True)

def save_user(user, match):
        saved_user = PotentialMatch(tinder_id=user.id, name=user.name, common_connections=len(user.common_connections),
                                 connection_count=0, age=user.age, distance=user.distance_km, matched=match)
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

#     user.bio # their biography
# user.name # their name
# user.photos # a list of photo URLs
# user.thumbnail #a list of thumbnails of photo URLS
# user.age # their age
# user.birth_date # their birth_date
# user.ping_time # last online
# user.distance_km # distane from you
# user.common_connections # friends in common
# user.connection_count # user facebook connection count
# user.common_interests # likes in common - returns a list of {'name':NAME, 'id':ID}
# user.get_photos(width=WIDTH) # a list of photo URLS with either of these widths ["84","172","320","640"]
# user.instagram_username # instagram username
# user.instagram_photos # a list of instagram photos with these fields for each photo: 'image','link','thumbnail'
# user.schools # list of schools
# user.jobs # list of jobs


    class Meta:
        database = db # This model uses the "people.db" database.

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