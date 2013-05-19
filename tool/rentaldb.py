import MySQLdb
import config

class SQL_init:

    def __init__(self):
        self.conn = MySQLdb.connect(host = config.host,user = config.user, passwd = config.passwd,db = config.db)

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

    # def create_attachment_table(self):
    #     # aid, rid, attribute, is_pic, s3key (5)
    #     cursor = self.conn.cursor()
    #     sql = "CREATE TABLE Attachment(aid serial NOT NULL AUTO_INCREMENT, rid integer NOT NULL, attribute VARCHAR(100), is_pic boolean NOT NULL DEFAULT true, s3key VARCHAR(500) NOT NULL, PRIMARY KEY (aid) )"
    #     try:
    #         cursor.execute(sql)
    #     except Exception,e:
    #         print e
    #     cursor.close()
    #     self.conn.commit()
    #     return 1

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

    def __init__(self):
        self.conn = MySQLdb.connect(host = config.host, user = config.user, passwd = config.passwd, db = config.db)
        self.uid = 0;

    def insert(self, value):
        username = value[0] or "NULL"
        password = value[1] or "NULL"
        email = value[2] or "NULL"
        phone = value[3] or "NULL"
        privilege = value[4] or "NULL"
        # INSERT INTO table_name 
        # VALUES (value1,value2,value3,...)
        cursor = self.conn.cursor()
        sql = "INSERT INTO `User`(username, password, email, phone, privilege) VALUES ('%s', '%s', '%s', '%s', '%s');" % (username, password, email, phone, privilege)
        # print sql
        try:
            cursor.execute(sql)
        except Exception,e:
            print e

        sql1 = "SELECT TABLE_ROWS FROM information_schema.tables WHERE table_name='User' AND table_schema = DATABASE();"
        cursor.execute(sql1)
        return_data = cursor.fetchall()
        cursor.close()
        self.uid = int(return_data[0][0])

        self.conn.commit()
        return 1

    # def search_by_uid
    # def search(self, table, which, where='', name=''):
    #     if which != '' and name != '' and where != '':
    #         sql = "select `%s` from `%s` where `%s` = '%s'" % (which, table, where, name)
    #     else:
    #         sql = "select * from %s" % table
    #     cursor = self.conn.cursor()
    #     cursor.execute(sql)
    #     alldata = cursor.fetchall()
    #     cursor.close()
    #     return alldata

#     def update(self, uid, value):
#     # UPDATE table_name
#     # SET column1=value, column2=value2,...
#     # WHERE some_column=some_value
#         cursor = self.conn.cursor()
#         sql = "UPDATE `User` SET ('%s, %s, %s, %s, %s, %s')" % (value[0], value[1], value[2], value[3], value[4], value[5])
#         sql = "UPDATE `User` SET `%s` = '%s' WHERE `%s` = '%s'" % (table, char, value, where, name)
#         try:
#             cursor.execute(sql)
#         except Exception,e:
#             print e
#         cursor.close()
#         self.conn.commit()
#         return 1

    def delete(self, uid):
        # DELETE FROM table_name WHERE some_column=some_value
        cursor = self.conn.cursor()
        sql = "DELETE FROM `User` WHERE `uid` IN ('%s')" % (uid)
        cursor.execute(sql)
        cursor.close()
        self.conn.commit()
        return 1


class Room:

    def __init__(self):
        self.conn = MySQLdb.connect(host = config.host, user = config.user, passwd = config.passwd, db = config.db)
        self.rid = 0;

    def insert(self, value):
        uid = value[0] or "NULL"
        tile = value[1] or "NULL"
        description = value[2] or "NULL"
        location = value[3] or "NULL"
        price = value[4] or "NULL"
        bucket = value[5] or "NULL"
        status = value[6] or "NULL"
        # INSERT INTO table_name 
        # VALUES (value1,value2,value3,...)
        cursor = self.conn.cursor()
        sql = "INSERT INTO `Room`(uid, title, description, location, price, bucket, status) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (uid, title, description, location, price, bucket, status)
        # print sql
        try:
            cursor.execute(sql)
        except Exception,e:
            print e

        sql1 = "SELECT TABLE_ROWS FROM information_schema.tables WHERE table_name='User' AND table_schema = DATABASE();"
        cursor.execute(sql1)
        return_data = cursor.fetchall()
        cursor.close()
        self.rid = int(return_data[0][0])

        self.conn.commit()
        return 1