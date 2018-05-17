import os

import pymysql

connection = pymysql.connect(host=os.getenv('DJANGO_DB_HOST', ''),
                user='root',
                password='123'
)
sql = open('scripts/Django-vod.sql', 'r').read()
try:
    with connection.cursor() as cursor:
        cursor.execute(sql)
    connection.commit()
finally:
    connection.close()