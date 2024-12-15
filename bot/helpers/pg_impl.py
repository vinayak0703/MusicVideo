import psycopg2
import datetime
import psycopg2.extras
import random

from .pg_db import DataBaseHandle

from config import Config

class MusicTable(DataBaseHandle):

    def __init__(self, dburl=None):
        if dburl is None:
            dburl = Config.DATABASE_URL
        super().__init__(dburl)

        music_schema = """CREATE TABLE IF NOT EXISTS music_table (
            id SERIAL PRIMARY KEY NOT NULL,
            title VARCHAR(50) NOT NULL,
            msg_id VARCHAR(50) DEFAULT NULL
        )"""

        cur = self.scur()
        try:
            cur.execute(music_schema)
        except psycopg2.errors.UniqueViolation:
            pass

        self._conn.commit()
        self.ccur(cur)

    def set_variable(self, title, msg_id):
        sql = "SELECT * FROM music_table WHERE title=%s"
        cur = self.scur()

        cur.execute(sql, (title,))

        sql = "INSERT INTO music_table(title,msg_id) VALUES(%s,%s)"

        cur.execute(sql, (title, msg_id))

        self.ccur(cur)

    def get_random(self):
        #sql = 'SELECT * FROM music_table'
        sql = "SELECT * FROM music_table ORDER BY id ASC LIMIT 1"
        cur = self.scur()

        item_id = None
        title = None
        msg_id = None

        cur.execute(sql)

        row = cur.fetchone()
        if row:
            item_id = row[0]
            title = row[1]
            msg_id = int(row[2])

        self.ccur(cur)

        return item_id, title, msg_id

    def drop_table(self):
        sql = 'DROP TABLE music_table'
        cur = self.scur()
        cur.execute(sql)
        self.ccur(cur)

    def drop_item(self, item_id):
        sql = 'DELETE FROM music_table where id=%s'

        cur = self.scur()
        cur.execute(sql, (item_id,))
        self.ccur(cur)
        

    def __del__(self):
        super().__del__()


class PhotoTable(DataBaseHandle):

    def __init__(self, dburl=None):
        if dburl is None:
            dburl = Config.DATABASE_URL
        super().__init__(dburl)

        photo_schema = """CREATE TABLE IF NOT EXISTS photo_table (
            id SERIAL PRIMARY KEY NOT NULL,
            msg_id VARCHAR(50) DEFAULT NULL
        )"""

        cur = self.scur()
        try:
            cur.execute(photo_schema)
        except psycopg2.errors.UniqueViolation:
            pass

        self._conn.commit()
        self.ccur(cur)

    def set_variable(self, msg_id):
        cur = self.scur()

        sql = "INSERT INTO photo_table(msg_id) VALUES(%s)"

        cur.execute(sql, (msg_id,))

        self.ccur(cur)

    def get_random(self):
        cur = self.scur()

        sql = "SELECT MIN(id), MAX(id) FROM photo_table"
        cur.execute(sql)

        min_id, max_id = cur.fetchone()

        random_id = random.randint(min_id, max_id)

        sql = "SELECT * FROM photo_table WHERE id >= %s LIMIT 1"
        cur.execute(sql, (random_id,))
        #sql = "SELECT * FROM photo_table ORDER BY id ASC LIMIT 1"
        #cur = self.scur()

        item_id = None
        msg_id = None

        row = cur.fetchone()
        if row:
            item_id = row[0]
            msg_id = int(row[1])

        self.ccur(cur)

        return msg_id

    def drop_table(self):
        sql = 'DROP TABLE photo_table'
        cur = self.scur()
        cur.execute(sql)
        self.ccur(cur)

    def drop_item(self, item_id):
        sql = 'DELETE FROM photo_table where id=%s'

        cur = self.scur()
        cur.execute(sql, (item_id,))
        self.ccur(cur)
        

    def __del__(self):
        super().__del__()

musictable = MusicTable()
phototable = PhotoTable()