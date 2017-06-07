#coding: utf-8
#!/usr/bin/python3.5

import pymysql
import urllib.request as UR
import xml.etree.ElementTree as ET

'''
This script is used for create and initialize a new database.
1.Create database and table [channel],[program].
2.Get channel id from channel URL.
3.Create tables using channel id as table name.
All create and insert commands will automatic skipped if the database/table/data already exists.
You can run this script again to update the database safely.
But still you have to delete the useless tables manually.

You can drop the old database if you want to start a fresh one.
Using the DropDatabase function at the end of this script.
Warning! You'll lost all the data after running drop command.
Think before you do it!
'''

# MySQL root password configuration.
passwd = '123'
# Channel API URL.
channel_url = 'http://api.deepepg.com/api/channel?secret=VYDcCe1s'
#channel_url = 'http://1.8.203.198:8080/EPG/channel?secret=VYDcCe1s'

class CreateDatabase:
    def __init__(self,database):
        self.db = database
        self.ConnectMySQL()
        self.cur = self.conn.cursor()

    # Connect to MySQL.
    def ConnectMySQL(self):
        try:
            self.conn = pymysql.connect(host='127.0.0.1', user='root', passwd=passwd,
                                        charset='utf8', cursorclass=pymysql.cursors.SSCursor)
            print('\033[32m' + 'MySQL connected...' + '\033[0m')

        except pymysql.MySQLError as err:
            print('\033[31m' + err.args[1] + '\033[0m')

    # MySQL command execute.
    def RunCommand(self, cmd):
        try:
            self.cur.execute(cmd)
        except pymysql.Error as err:
            print('\033[31m' + err.args[1] + '\033[0m')
        try:
            msg = self.cur.fetchall()
        except:
            msg = self.cur.fetchone()

        self.conn.commit()
        return msg

    def CreateDb(self,database):
        # Create database.
        self.RunCommand("CREATE DATABASE IF NOT EXISTS %s \
                        DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci" % self.db)

        self.RunCommand("use %s" % self.db)

        # Create table [channel].
        self.RunCommand("CREATE TABLE IF NOT EXISTS channel ( \
                          id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT, \
                          channel_id VARCHAR(45) NOT NULL, \
                          channel_name VARCHAR(200), \
                          rtmp_url VARCHAR(45), \
                          active INT(11) DEFAULT 0, \
                          start INT(11) DEFAULT 0, \
                          PID INT(11), \
                          PGID INT(11), \
                          client_ip VARCHAR(100), \
                          UNIQUE (channel_id), \
                          PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=utf8")

        # Create table [program].
        self.RunCommand("CREATE TABLE IF NOT EXISTS program ( \
                          channel_id VARCHAR(45) NOT NULL, \
                          start_time DATETIME, \
                          end_time DATETIME, \
                          url VARCHAR(200), \
                          title VARCHAR(200), \
                          finished INT(11) DEFAULT 0, \
                          event_id INT(11) NOT NULL, \
                          UNIQUE (url), \
                          UNIQUE (event_id), \
                          PRIMARY KEY (event_id)) ENGINE=InnoDB DEFAULT CHARSET=utf8")

    def GetChannel(self):
        self.tree = ET.parse(UR.urlopen(channel_url))
        self.root = self.tree.getroot()
        for self.channel in self.root.findall('channel'):
            self.channel_id = self.channel.get('id')
            self.channel_name = self.channel.find('name').text
            try:
                self.RunCommand("INSERT IGNORE INTO channel(channel_id,channel_name) \
                              VALUES ('%s','%s')" % (self.channel_id, self.channel_name))
                print('Get channel id <%s  %s>' % (self.channel_id,self.channel_name))
            except pymysql.MySQLError as err:
                print('\033[31m' + err.args[1] + '\033[0m')



    def DropDatabase(self,database):
        self.RunCommand("DROP DATABASE %s" % self.db)
        print("Database <%s> dropped" % self.db)

    def __del__(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        print('\033[31m' + 'MySQL disconnected...' + '\033[0m')




if __name__ == '__main__':
    database = 'tsrtmp'
    cd = CreateDatabase(database)
    cd.DropDatabase(database)  # <--- Uncomment if you need to use.
    cd.CreateDb(database)
    cd.GetChannel()
    print('All Done.')


