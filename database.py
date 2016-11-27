import sqlite3


class Database:
    """Simple database wrapper to store packages and the corresponding categories"""
    def __init__(self, file):
        self.con = sqlite3.connect(file)
        self.c = self.con.cursor()

        self.c.execute("""create table if not exists package (
            id integer primary key autoincrement,
            package text
        )""")

        self.c.execute("""create table if not exists category (
            id integer primary key autoincrement,
            category text
        )""")

        # Set up a table for a many-to-many relation
        self.c.execute("""create table if not exists package_category (
            package_id integer,
            category_id integer,
            foreign key(package_id) references package(id),
            foreign key(category_id) references category(id)
        )""")

    #region Insertion

    def insert_package(self, package, categories):
        """Inserts the given package and relates it to the given categories if it doesn't exist.
           Otherwise, the information is *not* updated, and False is returned"""

        # Ensure we have a list of categories
        if isinstance(categories, str):
            categories = [categories]

        if self.get_package_id(package) is None:
            # Insert the package
            self.c.execute('insert into package values (NULL, ?)', (package,))
            package_id = self.c.lastrowid

            # Insert new categories  or ignore them and retrieve their IDs
            for category_id in [self.insert_category(c) for c in categories]:
                # Add them to the many-to-many table
                self.c.execute('insert into package_category values(?, ?)',
                               (package_id, category_id))
            return True
        else:
            return False

    def insert_category(self, category):
        """Inserts or ignores the given category in the database and returns its ID"""
        result = self.get_category_id(category)
        if result is None:
            self.c.execute('insert into category values (NULL, ?)', (category,))
            result = self.c.lastrowid

        return result

    #endregion

    #region Getting

    def get_package_id(self, package):
        """Returns the package ID if package is found, None otherwise"""
        result = self.c.execute('select id from package where package=?', (package,)).fetchone()
        return result[0] if result else None

    def get_category_id(self, category):
        """Returns the category ID if category is found, None otherwise"""
        result = self.c.execute('select id from category where category=?', (category,)).fetchone()
        return result[0] if result else None

    def get_categories(self, package):
        """Returns a list containing strings representing the categories to which this package belongs to"""
        package_id = self.get_package_id(package)
        if package_id is not None:
            self.c.execute('select category_id from package_category where package_id=?',
                           (package_id,))

            return [             # Return a list made up from the categories text
                self.c.execute("""
                select category -- Select the category text
                from category   -- From the category table
                where id=?      -- Where the ID matches the returned many-to-many IDs
                """, (i[0],))    # With the first ID from the resulting ID tuple
                .fetchone()[0]   # (Fetch the first element, the category name, taking it out its tuple)
                for i in self.c.fetchall()  # Which IDs are returned in a list of tuples
            ]
        else:
            # Return an empty list if there is no package
            return []

    #endregion

    #region Others

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

    #endregion
