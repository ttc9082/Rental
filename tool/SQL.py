__author__ = 'TTc9082'
import MySQLdb
import config
class SQLtools:
    def __init__(self):
        self.conn = MySQLdb.connect(host=config.host,user=config.user,
                               passwd=config.passwd,db=config.db)
    def insert(self, table, char, value):
        cursor = self.conn.cursor()
        sql = "insert into %s(%s) values ('%s')" % (table, char, value)
        try:
            cursor.execute(sql)
        except Exception,e:
            print e
        cursor.close()
        self.conn.commit()
        return 1

    def lookup(self, table='videos', which='', where='', name=''):
        if which != '' and name != '' and where != '':
            sql = "select `%s` from `%s` where `%s` = '%s'" % (which, table, where, name)
        else:
            sql = "select * from %s" % table
        cursor = self.conn.cursor()
        cursor.execute(sql)
        alldata = cursor.fetchall()
        cursor.close()
        return alldata

    def update(self, table, char, value, where, name):
        cursor = self.conn.cursor()
        if type(value) != int:
            sql = "UPDATE `%s` SET `%s` = '%s' WHERE `%s` = '%s'" % (table, char, value, where, name)
        else:
            sql = "UPDATE `%s` SET `%s` = %s WHERE `%s` = '%s'" % (table, char, value, where, name)
            print 'updated int.'
        try:
            cursor.execute(sql)
        except Exception, e:
            print e
        cursor.close()
        self.conn.commit()
        print 'Updated!'
        return 1

    def sortdb(self):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM `videos` ORDER BY `rate` DESC LIMIT 0,1000"
        cursor.execute(sql)
        alldata = cursor.fetchall()
        cursor.close()
        return alldata

    def delraw(self, name):
        cursor = self.conn.cursor()
        sql = "DELETE FROM `videos` WHERE `key` IN ('%s')" % name
        cursor.execute(sql)
        cursor.close()
        self.conn.commit()
        return 1

