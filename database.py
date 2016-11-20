import sqlite3


class Database:
    """Simple database wrapper to store packages and the corresponding categories"""
    def __init__(self, file):
        self.con = sqlite3.connect(file)
        self.c = self.con.cursor()

        self.c.execute("""create table if not exists categories (
            package text primary key,
            categories text
        )""")

    def update_categories(self, package, categories):
        """Updates the categories (or category) for the given package"""
        if isinstance(categories, str):
            self.c.execute('insert or replace into categories values (?, ?)',
                           (package, categories))
        else:
            self.c.execute('insert or replace into categories values (?, ?)',
                           (package, ':'.join(categories)))

    def get_category(self, package):
        """If found, returns a list containing all the categories to which package belongs"""
        self.c.execute('select * from categories where package=?',
                       (package,))
        result = self.c.fetchone()
        if result:
            return result[1].split(':')

    def commit(self):
        """Commits changes on the database"""
        self.con.commit()

    def close(self):
        """Closes the database"""
        self.con.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
