from crawlers.crawler import Crawler
from database import Database


with Database('categories.db') as db:
    crawler = Crawler(db)

    print('Crawling F-Droid...')
    crawler.crawl_fdroid()

    print('Crawling Google Play...')
    crawler.crawl_gplay()

    print('Done!')
