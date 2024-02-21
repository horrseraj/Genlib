import peewee
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
    search_id = peewee.ForeignKeyField(null=False,
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


class Author(peewee.Model):
    id = peewee.AutoField(primary_key=True)
    name = peewee.CharField(max_length=100, null=False, verbose_name='Name')
    create_date = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = database_manager.db


class Book(peewee.Model):
    id = peewee.CharField(max_length=10, primary_key=True,
                          null=False, verbose_name='ID')
    title = peewee.TextField(null=False, verbose_name='Title')
    series = peewee.TextField(null=True, verbose_name='Series')
    publisher = peewee.TextField(null=True, verbose_name='Publisher')
    year = peewee.IntegerField(null=True, verbose_name='Year')
    language = peewee.CharField(
        max_length=50, null=True, verbose_name='Language')
    isbn10 = peewee.CharField(max_length=10, null=True, verbose_name='ISBN10')
    isbn13 = peewee.CharField(max_length=13, null=True, verbose_name='ISBN13')
    time_added = peewee.TextField(null=True, verbose_name='TimeAdded')
    time_modified = peewee.TextField(null=True, verbose_name='TimeModified')
    library = peewee.TextField(null=True, verbose_name='Library')
    library_issue = peewee.TextField(null=True, verbose_name='LibraryIssue')
    size = peewee.CharField(max_length=50, null=True, verbose_name='Size')
    extension = peewee.CharField(
        max_length=10, null=True, verbose_name='Extension')
    worse_versions = peewee.TextField(null=True, verbose_name='Worseversions')
    Desr_old_vers = peewee.TextField(null=True, verbose_name='DesrOldVers')
    commentary = peewee.TextField(null=True, verbose_name='Commentary')
    topic = peewee.TextField(null=True, verbose_name='Topic')
    tags = peewee.TextField(null=True, verbose_name='Tags')
    periodical = peewee.TextField(null=True, verbose_name='Periodical')
    city = peewee.TextField(null=True, verbose_name='City')
    edition = peewee.TextField(null=True, verbose_name='Edition')
    pages_biblio = peewee.IntegerField(null=True, verbose_name='PagesBiblio')
    pages_tech = peewee.IntegerField(null=True, verbose_name='PagesTech')
    html = peewee.TextField(verbose_name='HTML')

    class Meta:
        database = database_manager.db


class BookAuthor(peewee.Model):
    book_id = peewee.ForeignKeyField(Book, backref='authors')
    author_id = peewee.ForeignKeyField(Author, backref='books')

    class Meta:
        database = database_manager.db
        primary_key = peewee.CompositeKey('book_id', 'author_id')
