from peewee import *
import datetime
import os
from flask_login import UserMixin
from playhouse.db_url import connect

# DATABASE = SqliteDatabase('items.sqlite')

if 'ON_HEROKU' in os.environ: # later we will manually add this env var
                              # in heroku so we can write this code
  DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this
                                                     # env var for you
                                                     # when you provision the
                                                     # Heroku Postgres Add-on
else:
  DATABASE = SqliteDatabase('items.sqlite')

class User(UserMixin, Model):
    username=CharField(unique=True)
    password=CharField()

    class Meta:
        database = DATABASE

class Item(Model):
    name = CharField()
    #create a relationship between an item and a user:
    uploader = ForeignKeyField(User, backref='items')
    link = CharField()
    description = CharField()
    media_link = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    # Creating table when we're initializing
    DATABASE.create_tables([User, Item], safe=True)
    print("TABLES Created")
    DATABASE.close()
