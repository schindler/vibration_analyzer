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
        cur.execute("CREATE TABLE Data (id INTEGER primary key not null, x REAL, y REAL, z REAL, t INTEGER)")
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

    def add(self, acceleration, temperature):
        """
            Adds a new record
            >>> Store().add([1.5,2,3], 26)
            >>> Store().last()[4]
            26
        """
        cur = self.connection.cursor()
        cur.execute("INSERT INTO Data VALUES (NULL, ?, ?, ?, ?)", 
            (acceleration[0], acceleration[1], acceleration[2], temperature,))
        cur = None
        self.connection.commit()

    def add_all(self, rows):
        """
            Add all
            param rows list of tuple [(x,y,z,t)]

            >>> s = Store()
            >>> r = [(1,2,3,21),(5,6,7,22),(8,9,10,23)]
            >>> s.add_all(r)
        """
        cur = self.connection.cursor()
        try:
            cur.execute("begin")
            for row in rows:
                cur.execute("INSERT INTO Data VALUES (NULL, ?, ?, ?, ?)", row)
            cur.execute("commit")
        except sql.Error as error:
            cur.execute("rollback")
            raise error
        finally:
            cur = None

    def last(self):
        """
            Gets last record
        """
        cur = self.connection.cursor()
        return cur.execute("SELECT * from Data order by id desc limit 1").fetchone()
          