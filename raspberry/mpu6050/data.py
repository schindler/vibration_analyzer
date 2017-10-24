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
        cur.execute("CREATE TABLE IF NOT EXISTS Session (id INTEGER primary key not null, timestamp DATETIME)")
        cur.execute("CREATE TABLE IF NOT EXISTS Data (id INTEGER primary key not null, session_id INTEGER not null, x REAL, y REAL, z REAL, t REAL, timestamp DATETIME)")
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
        self.session_id = self.session()
        assert self.session_id >= 0, "Init Store failure!"
        

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.connection.disconnect()

    def session(self):
        """
        Creates a new session
        """    
        self.cursor = self.connection.cursor()  
        self.cursor.execute("INSERT INTO Session VALUES (NULL, STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'))")
        self.commit()
        return self.cursor.execute("SELECT id from Session order by id desc limit 1").fetchone()[0]

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
            >>> s.last()[5]
            26.0
        """

        self.cursor.execute("INSERT INTO Data VALUES (NULL, ?, ?, ?, ?, ?, STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'))", (self.session_id,)+row)


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
            self.cursor.execute("rollback")
            raise error

    def last(self):
        """
            Gets last record
        """
        return self.cursor.execute("SELECT * from Data order by id desc limit 1").fetchone()
          