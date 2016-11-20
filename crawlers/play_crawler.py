from urllib.request import urlopen
from urllib.error import HTTPError
import re

# Nothing must be formatted
PLAY_URL = "https://play.google.com/store/apps"

CATEGORY_RE = re.compile(
    r'/store/apps/category/(\w+)')


# You must format a "CATEGORY"
PLAY_TOP_PAID = "https://play.google.com/store/apps/category/{}/collection/topselling_paid"
PLAY_TOP_FREE = "https://play.google.com/store/apps/category/{}/collection/topselling_free"

PACKAGE_RE = re.compile(
    r'href="/store/apps/details\?id=(.+?)"')


# You must format a "com.android.package"
PLAY_PACKAGE_URL = "https://play.google.com/store/apps/details?id={}&hl=en"

PLAY_RE = re.compile(
    r'<a class="document-subtitle category" href="/store/apps/category/(\w+)">')


class PlayCrawler:
    """Crawler for the Google Play site, being able to retrieve all
       the available categories, all the packages for a given category
       and also all the categories for a given package"""
    @staticmethod
    def get_all_categories():
        """Crawls the main Google Play website to determine all the available categories"""
        categories = set()
        for m in PlayCrawler.match_url(PLAY_URL, CATEGORY_RE):
            categories.add(m.group(1))

        return categories

    @staticmethod
    def get_all_packages(category):
        """Crawls the Google Play website for the given category returning all the packages"""
        packages = set()
        for m in PlayCrawler.match_url(PLAY_TOP_PAID.format(category), PACKAGE_RE):
            packages.add(m.group(1))
        for m in PlayCrawler.match_url(PLAY_TOP_FREE.format(category), PACKAGE_RE):
            packages.add(m.group(1))

        return packages

    @staticmethod
    def get_categories(package):
        """Returns all the categories to which the given package belongs"""
        return [m.group(1) for m in
                PlayCrawler.match_url(PLAY_PACKAGE_URL.format(package), PLAY_RE)]

    @staticmethod
    def match_url(url, regex):
        """Downloads an HTML string from url and returns an iterable object
           with all the matches for the given regex"""
        try:
            html = urlopen(url).read().decode('utf-8')
            return regex.finditer(html)
        except HTTPError:  # 404
            return []
