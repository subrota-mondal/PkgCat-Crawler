import os
import urllib.request
import xml.etree.ElementTree as etree
import zipfile


URL_FDROID = 'http://f-droid.org/repo/index.jar'


class FDroidCrawler:
    """Crawler that looks into F-Droid's package index"""
    @staticmethod
    def yield_packages_categories():
        """Crawls the F-Droid packages index and yielding tuples
           containing (package string, categories list) as a result"""

        # Download F-Droid's apps index.jar
        urllib.request.urlretrieve(URL_FDROID, 'index.jar')

        # Extract index.xml from the index.jar
        zfile = zipfile.ZipFile('index.jar', 'r')
        with open('index.xml', 'wb') as f:
            f.write(zfile.read('index.xml'))

        # Parse the HTML and fill the database
        tree = etree.parse('index.xml')
        for app in tree.getroot().findall('application'):
            # Child also has the attrib 'id', which contains the package name
            # It can be retrieved with `child.get('attribute name')`
            #
            # `child.find('tag')` on the other hands finds the first tag
            package = app.find('id').text

            # Replace ' & ' as two categories
            # Store the categories in UPPER CASE
            # Do not use plural, strip the 'S'
            categories = app.find('categories').text \
                .replace(' & ', ':').upper().rstrip('S').split(',')

            yield package, categories

        # Clean up
        os.remove('index.jar')
        os.remove('index.xml')
