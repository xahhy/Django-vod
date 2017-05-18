#coding: utf-8
#!/usr/bin/python3.5

import pymysql
import django
import os
import urllib.request as UR
import xml.etree.ElementTree as ET
'''
if user delete the table in the database, you need to run 2 lines commands below to create the table:
python manage.py migrate --fake appname zero
python manage.py migrate appname
'''
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
# channel_url = 'http://api.deepepg.com/api/channel?secret=RKG8zGWy'
channel_url = 'http://1.8.203.198:8080/EPG/channel?secret=VYDcCe1s'

class CreateDatabase:
    def GetChannel(self):
        self.tree = ET.parse(UR.urlopen(channel_url))
        self.root = self.tree.getroot()
        for self.channel in self.root.findall('channel'):
            self.channel_id = self.channel.get('id')
            self.channel_name = self.channel.find('name').text
            print(self.channel_id)
            print(self.channel_name)
            print("------------")
            #try:
            Channel.objects.create(channel_id=self.channel_id,channel_name=self.channel_name)
                #self.RunCommand("INSERT IGNORE INTO channel(channel_id,channel_name) \
                 #             VALUES ('%s','%s')" % (self.channel_id, self.channel_name))
                #print('Get channel id <%s  %s>' % (self.channel_id,self.channel_name))
            #except pymysql.MySQLError as err:
            #    print('\033[31m' + err.args[1] + '\033[0m')



    def DropDatabase(self,database):
        self.RunCommand("DROP DATABASE %s" % self.db)
        print("Database <%s> dropped" % self.db)



if __name__ == '__main__':
    database = 'tsrtmp'
    print(database)
    pymysql.install_as_MySQLdb()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()
    from epg.models import Channel
    from django.db import models

    cd = CreateDatabase()
    #cd.DropDatabase(database)  # <--- Uncomment if you need to use.
    #cd.CreateDb(database)
    cd.GetChannel()
    print('All Done.')


