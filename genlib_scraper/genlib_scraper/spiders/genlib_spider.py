import scrapy

from genlib_scraper.items import BookItem
from models import SearchKey, SearchResult, Author, Book, BookAuthor


class GenlibSpider(scrapy.Spider):
    name = 'genlib'
    allowed_domains = ['genlib.is']

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            # 'Referer': 'http://www.example.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # Add other headers as needed
        }
        search_key = getattr(self, 'search_key', None)
        if search_key:
            new_search = SearchKey.create(search_key=search_key)
            search_id = new_search.id
            url = f'https://libgen.rs/search.php?req={
                search_key}&open=0&res=25&view=simple&phrase=1&column=def'  # &page={}'
            yield scrapy.Request(url, callback=self.parse, headers=headers, meta={'search_id': search_id})

    def parse(self, response):
        # Extracting search results
        search_id = response.meta['search_id']
        # Skip the first <tr> element (header)
        trs = response.css('table.c tr')[1:]
        for tr in trs:  
            # Extracting data from each <td> element within the <tr> element
            book_id = tr.css('td:nth-of-type(1)::text').get()
            elements = tr.css('td:nth-of-type(2)')
            author_names = elements.css('a::text').getall()
            authors = ', '.join(author_names)
            title = tr.css('td:nth-of-type(3) a::text').get()
            link = tr.css('td:nth-child(3) a::attr(href)').get()
            publisher = tr.css('td:nth-of-type(4)::text').get()
            year = tr.css('td:nth-of-type(5)::text').get()
            pages = tr.css('td:nth-of-type(6)::text').get()
            language = tr.css('td:nth-of-type(7)::text').get()
            size = tr.css('td:nth-of-type(8)::text').get()
            extension = tr.css('td:nth-of-type(9)::text').get()

            try:
                year = int(year)
            except (TypeError, ValueError):
                year = 0
            try:
                pages = int(pages)
            except (TypeError, ValueError):
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
            # Check to see if this book_id exists
            try:
                Book.get(Book.id == book_id)
            except Book.DoesNotExist:
                link = f'https://libgen.rs/{link}'
                yield scrapy.Request(link, callback=self.parse_book, meta={'authors': author_names})

    def parse_book(self, response):
        self.logger.info('Entering parse_book method')
        self.logger.info('Response URL: %s', response.url)
        self.logger.info('Response status: %s', response.status)
        
        html = response.text
        # Select the <tr> elements
        tr_elements = response.css('table tbody tr')[1:15]
        for tr_index, tr in enumerate(tr_elements, start=2):
            # Select the <td> elements within the <tr>
            td_elements = tr.css('td')
            for td_index, td in enumerate(td_elements, start=1):
                if tr_index == 2 and td_index == 3:
                    title = td.css('a::text').get()
                if tr_index == 4 and td_index == 2:
                    series = td.css('::text').get()
                if tr_index == 4 and td_index == 4:
                    periodical = td.css('::text').get()
                if tr_index == 5 and td_index == 2:
                    publisher = td.css('::text').get()
                if tr_index == 5 and td_index == 4:
                    city = td.css('::text').get()
                if tr_index == 6 and td_index == 2:
                    year = td.css('::text').get()
                if tr_index == 6 and td_index == 4:
                    edition = td.css('::text').get()
                if tr_index == 7 and td_index == 2:
                    language = td.css('::text').get()
                if tr_index == 7 and td_index == 4:
                    pages = td.css('::text').get()
                    pages_biblio, pages_tech = pages.split('\\')
                if tr_index == 8 and td_index == 2:
                    isbn = td.css('::text').get()
                    isbn10, isbn13 = isbn.split(',')
                if tr_index == 8 and td_index == 4:
                    id = td.css('::text').get()
                if tr_index == 9 and td_index == 2:
                    time_added = td.css('::text').get()
                if tr_index == 9 and td_index == 4:
                    time_modified = td.css('::text').get()
                if tr_index == 10 and td_index == 2:
                    library = td.css('::text').get()
                if tr_index == 10 and td_index == 4:
                    library_issue = td.css('::text').get()
                if tr_index == 11 and td_index == 2:
                    size = td.css('::text').get()
                if tr_index == 11 and td_index == 4:
                    extension = td.css('::text').get()
                if tr_index == 12 and td_index == 2:
                    worse_versions = td.css('::text').get()
                if tr_index == 13 and td_index == 2:
                    Desr_old_vers = td.css('::text').get()
                if tr_index == 13 and td_index == 4:
                    library_issue = td.css('::text').get()
                if tr_index == 14 and td_index == 2:
                    commentary = td.css('::text').get()
                if tr_index == 15 and td_index == 2:
                    topic = td.css('::text').get()
                if tr_index == 15 and td_index == 4:
                    tags = td.css('::text').get()
        # Create an instance of Book and save it to the database
        new_book = Book.create(
            id=id,
            title=title,
            series=series,
            publisher=publisher,
            year=year,
            language=language,
            isbn10=isbn10,
            isbn13=isbn13,
            time_added=time_added,
            time_modified=time_modified,
            library=library,
            library_issue=library_issue,
            size=size,
            extension=extension,
            worse_versions=worse_versions,
            Desr_old_vers=Desr_old_vers,
            commentary=commentary,
            topic=topic,
            tags=tags,
            periodical=periodical,
            city=city,
            edition=edition,
            pages_biblio=pages_biblio,
            pages_tech=pages_tech,
            html=html
        )
        # Insert Authors if they already dont exist
        author_names = response.meta['author_names']
        for auth in author_names:
            try:
                author = Author.get(Author.name == auth)
            except Author.DoesNotExist:
                author = Author.create(name=auth)
            finally:
                # Insert BookAuthor 
                BookAuthor.create(book_id=new_book.id,
                                  author_id=author.id)

        yield Book
