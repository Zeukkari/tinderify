from playhouse.migrate import *

my_db = SqliteDatabase('tinder.db')
migrator = SqliteMigrator(my_db)

#
# title_field = CharField(default='')
# status_field = IntegerField(null=True)
liked = BooleanField(null=True)
swipe_date = DateTimeField(null=True)
match_date = DateTimeField(null=True)
match_id = CharField(unique=True, null=True)
message_id = CharField(null=True) # Tinder internal message id
with my_db.transaction():
    migrate(
        # migrator.add_column('PotentialMatch', 'liked', liked),
        # migrator.add_column('PotentialMatch', 'swipe_date', swipe_date),
        # migrator.add_index('PotentialMatch', ('tinder_id',), True),
        # migrator.add_index('Photo', ('tinder_id',), True),
        # migrator.add_index('PotentialMatch', ('tinder_id',), True),
        migrator.add_column('Conversation', 'message_id', message_id),
        # migrator.add_column('some_table', 'status', status_field),
        # migrator.drop_column('some_table', 'old_column'),
    )
