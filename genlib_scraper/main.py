from scrapy.crawler import CrawlerProcess
import argparse
from datetime import datetime
import os
import sys

from genlib_scraper.spiders.genlib_spider import GenlibSpider
from models import SearchKey, SearchResult, Author
from database_manager import DatabaseManager
import local_settings


database_manager = DatabaseManager(
    database_name=local_settings.DATABASE['name'],
    user=local_settings.DATABASE['user'],
    password=local_settings.DATABASE['password'],
    host=local_settings.DATABASE['host'],
    port=local_settings.DATABASE['port'],
)


def run_spider(key, format, path):
    output_filename = f'{path}/output.{format}'
    process = CrawlerProcess(settings={
        'FEED_FORMAT': format,        
        'FEED_URI': output_filename,
    })
    process.crawl(GenlibSpider, search_key=key)
    process.start()


def validate_arguments(args):
    if not args.key:
        print("Error: Search key is missing.")
        sys.exit(1)
    if not os.path.exists('./output'):
        os.makedirs('./output')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='main.py')
    parser.add_argument(
        '-s', '--key', help='Search key for Genlib Spider', required=True)
    parser.add_argument('-f', '--format', default='json', choices=['json', 'csv', 'xml'],
                        help='Output format for scraped data (default: json)')
    args = parser.parse_args()

    validate_arguments(args)

    now = datetime.now()
    path = f'./output/{args.key}_{now.strftime("%Y%m%d-%H%M%S")}'

    try:
        os.makedirs(path)

        database_manager.create_tables(models=[SearchKey, SearchResult, Author])

        run_spider(args.key, args.format, path)
    except OSError as e:
        print(f"Error: Failed to create output directory: {e}")
        sys.exit(1)
    except Exception as error:
        print('Error', error)
    finally:
        # closing database connection.
        if database_manager.db:
            database_manager.db.close()
            print('Database connection is closed')
