import scrapy

class BookItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    publication_year = scrapy.Field()
    file_urls = scrapy.Field()
    image_urls = scrapy.Field()
