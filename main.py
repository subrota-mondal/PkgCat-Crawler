from crawlers.crawler import Crawler
from database import Database


def display_added_count(count):
    if count > 1:
        print(count, 'new packages added.')
    elif count == 1:
        print('One new package added.')
    else:
        print('No new packages added.')


with Database('categories.db') as db:
    crawler = Crawler(db)

    print('Crawling F-Droid...')
    display_added_count(crawler.crawl_fdroid())

    print('Crawling Google Play...')
    display_added_count(crawler.crawl_gplay())

    print('Done!')
