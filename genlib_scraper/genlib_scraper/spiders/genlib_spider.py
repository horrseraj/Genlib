import scrapy

from genlib_scraper.items import BookItem
#from genlib_scraper.models import SearchKey, SearchResult
from models import SearchKey, SearchResult


class GenlibSpider(scrapy.Spider):
    name = 'genlib'
    allowed_domains = ['genlib.is']

    def start_requests(self):
        search_key = getattr(self, 'search_key', None)
        if search_key:
            new_search = SearchKey.create(search_key=search_key)
            search_id = new_search.id
            url = f'https://genlib.is/search.php?req={search_key}'  # &page={}'
            yield scrapy.Request(url, self.parse, meta={'search_id': search_id})

    def parse(self, response):
        # Extracting search results
        search_id = response.meta['search_id']
        for tr in response.css('table.c tr'):
            # Extracting data from each <td> element within the <tr> element
            book_id = tr.css('td:nth-of-type(1)::text').get()
            authors = tr.css('td:nth-of-type(2) a::text').get()
            title = tr.css('td:nth-of-type(3) a::text').get()
            publisher = tr.css('td:nth-of-type(4)::text').get()
            year = tr.css('td:nth-of-type(5)::text').get()
            pages = tr.css('td:nth-of-type(6)::text').get()
            language = tr.css('td:nth-of-type(7)::text').get()
            size = tr.css('td:nth-of-type(8)::text').get()
            extension = tr.css('td:nth-of-type(9)::text').get()

            # Perform any necessary data type conversion
            try:
                year= int(year)
            except ValueError:
                year = 0
            try:
                pages= int(pages)
            except ValueError:
                pages = 0

            # Create an instance of SearchResult and save it to the database
            result = SearchResult.create(
                search_id=search_id,
                book_id=book_id,
                title=title,
                authors=authors,
                publisher=publisher,
                year=year,
                pages=pages,
                language=language,
                size=size,
                extension=extension
            )

        # book_links = response.css(
        #     'table.c td:nth-child(3) a::attr(href)').extract()

        # for link in book_links:
        #     # , meta={'title': title})
        #     yield scrapy.Request(link, callback=self.parse_book)

    def parse_book(self, response):
        title = response.meta.get('title')
        author = response.css('h2::text').get()
        publication_year = response.css('table td:nth-of-type(1)::text').get()

        item = BookItem()
        item['title'] = title
        item['author'] = author
        item['publication_year'] = publication_year
        # Assuming the book file is downloadable from the book page
        item['file_urls'] = [response.url]
        item['image_urls'] = [response.urljoin(image_url) for image_url in response.css(
            'img[src*=cover]::attr(src)').getall()]

        yield item
