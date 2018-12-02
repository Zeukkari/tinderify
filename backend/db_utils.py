### This functions are for converting database objects to objects that are used by the browser as JSON


def get_thumbnails(thumbnails):
    return [thumbnail.url for thumbnail in thumbnails]


def get_photos(photos):
    return [{"url": photo.url, "id": photo.id} for photo in photos]


def get_conversation(conversations):
    return [{"id": message.id, "message": message.body, "sender": message.sender, "sent": message.sent} for message in
            conversations]


def database_user_to_object(self, user):
    return {"name": user.name, "thumbnails": self.get_thumbnails(user.thumbnails),
            "photos": self.get_photos(user.photos), "messages": self.get_conversation_db(user.conversation),
            "id": user.tinder_id, "match_id": user.match_id, "bio": user.bio, "age": user.age,
            "last_activity_date": user.last_activity_date, "common_connections": user.common_connections,
            "matched": user.matched}
