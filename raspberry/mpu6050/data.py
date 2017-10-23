"""
    Data Store
"""

import sqlite3 as sql

def create_db(basename):
    """
        Creates connection with database and update schema
    """

    con = sql.connect(basename)
    cur = con.cursor()

    try:
        cur.execute("CREATE TABLE Data (id INTEGER primary key not null, x REAL, y REAL, z REAL, t REAL, timestamp DATETIME)")
        con.commit()
    except sql.OperationalError:
        pass

    return con

class Store(object):
    """
        Store all data read
    """
    def __init__(self):
        self.connection = create_db("datastore.db")
        self.connection.isolation_level = None
        self.cursor = self.connection.cursor()
        self.cursor.execute("begin")

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.connection.disconnect()

    def commit(self):
        """
            commit
        """
        self.connection.commit()
        self.cursor = self.connection.cursor()
        self.cursor.execute("begin")

    def add(self, row):
        """
            Adds a new record
            >>> s = Store()
            >>> s.add((1.5,2,3,26))
            >>> s.commit()
            >>> s.last()[4]
            26.0
        """
        self.cursor.execute("INSERT INTO Data VALUES (NULL, ?, ?, ?, ?, STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'))", row)


    def add_all(self, rows):
        """
            Add all
            param rows list of tuple [(x,y,z,t)]

            >>> s = Store()
            >>> r = [(1,2,3,21),(5,6,7,22),(8,9,10,23)]
            >>> s.add_all(r)
        """
        try:
            for row in rows:
                self.add(row)
            self.commit()
        except sql.Error as error:
            cursor.execute("rollback")
            raise error

    def last(self):
        """
            Gets last record
        """
        return self.cursor.execute("SELECT * from Data order by id desc limit 1").fetchone()
          