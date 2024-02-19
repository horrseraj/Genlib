import peewee  # , PostgresqlDatabase, TextField
from datetime import datetime

from database_manager import DatabaseManager
import local_settings

database_manager = DatabaseManager(
    database_name=local_settings.DATABASE['name'],
    user=local_settings.DATABASE['user'],
    password=local_settings.DATABASE['password'],
    host=local_settings.DATABASE['host'],
    port=local_settings.DATABASE['port'],
)

class SearchKey(peewee.Model):
    id = peewee.AutoField(primary_key=True)
    search_key = peewee.TextField(null=False, verbose_name='SearchKey')
    search_date = peewee.DateTimeField(default=datetime.now)

class Meta:
        database = database_manager.db    


class SearchResult(peewee.Model):
    search_id = peewee.ForeignKeyField(
        model=SearchKey, backref='results', on_delete='CASCADE')
    book_id = peewee.CharField(
        max_length=10, null=False, verbose_name='BookId')
    authors = peewee.TextField(null=True, verbose_name='Authors')
    title = peewee.TextField(null=True, verbose_name='Title')
    publisher = peewee.TextField(null=True, verbose_name='Publisher')
    year = peewee.IntegerField(null=True, verbose_name='Year')
    pages = peewee.IntegerField(null=True, verbose_name='Pages')
    language = peewee.CharField(
        max_length=50, null=True, verbose_name='Language')
    size = peewee.CharField(max_length=50, null=True, verbose_name='Size')
    extension = peewee.CharField(
        max_length=50, null=True, verbose_name='Extension')

    class Meta:
        database = database_manager.db
