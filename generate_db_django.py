#coding: utf-8
#!/usr/bin/python3.5

import pymysql
import django
import os
from vodmanagement.models import *
import urllib.request as UR
import xml.etree.ElementTree as ET

# scan all mp4 files under a given directory,
# and create a Vod object for each file,
# Vod.title equals to file name as default
# file name can't be the same
class CreadVod:
    def __init__(self):
        self.objs = Vod.objects.all()

    def



if __name__ == '__main__':
    database = 'tsrtmp'
    print(database)
    pymysql.install_as_MySQLdb()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()
    vods = CreadVod()
    print('All Done.')


