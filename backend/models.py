from peewee import *
import datetime
from flask_login import UserMixin

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
