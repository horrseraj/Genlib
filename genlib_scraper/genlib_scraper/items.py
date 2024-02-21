import scrapy


class SearchKeyItem(scrapy.Item):
    id = scrapy.Field()
    search_key = scrapy.Field()
    search_date = scrapy.Field()


class SearchResultItem(scrapy.Item):
    search_id = scrapy.Field()
    book_id = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    publisher = scrapy.Field()
    year = scrapy.Field()
    pages = scrapy.Field()
    language = scrapy.Field()
    size = scrapy.Field()
    extension = scrapy.Field()


class BookItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    series = scrapy.Field()
    publisher = scrapy.Field()
    year = scrapy.Field()
    language = scrapy.Field()
    isbn10 = scrapy.Field()
    isbn13 = scrapy.Field()
    time_added = scrapy.Field()
    time_modified = scrapy.Field()
    library = scrapy.Field()
    library_issue = scrapy.Field()
    size = scrapy.Field()
    extension = scrapy.Field()
    worse_versions = scrapy.Field()
    Desr_old_vers = scrapy.Field()
    commentary = scrapy.Field()
    topic = scrapy.Field()
    tags = scrapy.Field()
    periodical = scrapy.Field()
    city = scrapy.Field()
    edition = scrapy.Field()
    pages_biblio = scrapy.Field()
    pages_tech = scrapy.Field()
    html = scrapy.Field()


class AuthorItem(scrapy.Item):
    name = scrapy.Field()


class BookAuthorItem(scrapy.Item):
    book_id = scrapy.Field()
    author_id = scrapy.Field()
