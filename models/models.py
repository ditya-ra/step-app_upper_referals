import os

from peewee import Model, CharField, SqliteDatabase,ForeignKeyField, DateTimeField

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db = SqliteDatabase(os.path.join(BASE_DIR, 'db'))


class BaseModel(Model):
    class Meta:
        database = db


class Proxy(BaseModel):
    host = CharField()
    status = CharField()

    class Meta:
        table_name = 'proxies'


class Account(BaseModel):
    ref_code = CharField()

    class Meta:
        table_name = 'accounts'


class Statistic(BaseModel):
    date = DateTimeField()
    account = ForeignKeyField(Account)
    proxy = ForeignKeyField(Proxy)

    class Meta:
        table_name = 'statistics'
