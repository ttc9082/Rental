import MySQLdb
import config

class SETUP:
    conn = MySQLdb.connect(host = config.host, user = config.user, passwd = config.passwd, db = config.db)

    @classmethod
    def create_user_table(self):
        # uid, username, password, email, phone, privilege (6)
        cursor = self.conn.cursor()
        sql = "CREATE TABLE User(uid serial NOT NULL AUTO_INCREMENT, username VARCHAR(100) NOT NULL, password VARCHAR(100) NOT NULL, email VARCHAR(100), phone VARCHAR(100), privilege integer NOT NULL DEFAULT 0, PRIMARY KEY (uid) )"
        try:
            cursor.execute(sql)
        except Exception,e:
            print e
        cursor.close()
        self.conn.commit()
        return 1

    @classmethod
    def create_room_table(self):
        # rid, uid, title, description, location, price, bucket, status (8)
        cursor = self.conn.cursor()
        sql = "CREATE TABLE Room(rid serial NOT NULL AUTO_INCREMENT, uid integer NOT NULL, title VARCHAR(100) NOT NULL, description VARCHAR(1000), location VARCHAR(500), price integer, bucket VARCHAR(100) NOT NULL, status boolean NOT NULL DEFAULT false, PRIMARY KEY (rid) )"
        try:
            cursor.execute(sql)
        except Exception,e:
            print e
        cursor.close()
        self.conn.commit()
        return 1

    @classmethod
    def drop_tables(self):
        cursor = self.conn.cursor()
        sql = "DROP TABLE User; DROP TABLE Room;"
        try:
            cursor.execute(sql)
        except Exception,e:
            print e
        cursor.close()
        self.conn.commit()
        return 1


class User:
    conn = MySQLdb.connect(host = config.host, user = config.user, passwd = config.passwd, db = config.db)

    @classmethod
    def insert(self, value):
        username, password, email, phone, privilege = value
        cursor = self.conn.cursor()
        sql = "INSERT INTO `User`(username, password, email, phone, privilege) VALUES ('%s', '%s', '%s', '%s', '%s');" % (username, password, email, phone, privilege)
        # print sql
        try:
            cursor.execute(sql)
        except Exception,e:
            print e
        self.conn.commit()
        return 1

    @classmethod
    def validate_passwd(self, username):
        sql = "SELECT `password` FROM `User` WHERE `username` = '%s'" %(username)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        ps = cursor.fetchall()
        cursor.close()
        lst = [x for x, in ps]
        return lst


class Room:
    conn = MySQLdb.connect(host = config.host, user = config.user, passwd = config.passwd, db = config.db)

    @classmethod
    def insert(self, value):
        uid, title, description, location, price, bucket, status = value
        cursor = self.conn.cursor()
        sql = "INSERT INTO `Room`(uid, title, description, location, price, bucket, status) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (uid, title, description, location, price, bucket, status)
        try:
            cursor.execute(sql)
        except Exception,e:
            print e
        self.conn.commit()
        return 1

    @classmethod
    def show_all(self):
        sql = "SELECT * FROM `Room`;"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return data

    @classmethod
    def show_my_rooms(self, uid):
        sql = "SELECT * FROM `Room` WHERE `uid` = '%s'" % (uid)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return data
