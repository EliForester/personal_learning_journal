from peewee import *

db = SqliteDatabase('learning_journal.db')


class BaseModel(Model):

    class Meta:
        database = db


class Entry(BaseModel):
    title = CharField(null=False, unique=True)
    date = DateField(null=False)
    time_spent = IntegerField(null=False)
    learned = TextField(null=True)
    resources = TextField(null=True)


if __name__ == '__main__':
    try:
        Entry.create_table()
    except DatabaseError:
        print('Table already exists')
