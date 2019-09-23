from peewee import *

db = SqliteDatabase('chainsaw_jugglers_peewee_db.sqlite')

# Create model class. 
class Juggler(Model):
    name = CharField()
    country = CharField()
    numberOfCatches = IntegerField()

    # Link this model to the database
    class Meta:
        database = db

    def __str__(self):
        return f'{self.name} from {self.country} holds a record of {self.numberOfCatches} catches.'
