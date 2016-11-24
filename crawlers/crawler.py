from crawlers import FDroidCrawler, PlayCrawler


class Crawler:
    """Crawler that combines Google Play and F-Droid crawlers
       to fill in a given database"""
    def __init__(self, db):
        self.db = db

    def crawl_gplay(self):
        """Crawls the Google Play website updating the database
           with the top applications for each available category"""
        crawler = PlayCrawler()

        categories = crawler.get_all_categories()
        for i, category in enumerate(categories):
            i += 1  # 1-index based

            print('Retrieving packages for category {} ({}/{})'
                  .format(category, i, len(categories)))

            for pkg in crawler.get_all_packages(category):
                self.db.insert_package(pkg, category)
            self.db.commit()

    def crawl_fdroid(self):
        """Crawls the F-Droid package index website updating the database
           with the all the available applications on F-Droid"""
        crawler = FDroidCrawler()
        for pkg, categories in crawler.yield_packages_categories():
            self.db.insert_package(pkg, categories)

        self.db.commit()
