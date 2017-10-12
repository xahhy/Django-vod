
# Django-vod
Use Django to create a vod(video on demand) manage system
Based on Bootstrap3

# Use MySQL db
reference:
> www.centoscn.com/mysql/2016/0315/6844.html
1. 
```
#install dependencies
yum search libaio\
yum install libaio\
```
2. 
```
#check mysql was installed or not\
yum list installed | grep mysql\
#if installed then remove them\
yum remove mysql-libs\
```
3.
```
#download mysql yum repository
wget http://dev.mysql.com/get/mysql-community-release-el7-5.noarch.rpm\
#mannuly install repository\
yum localinstall mysql-community-release-el7-5.noarch.rpm\
#check if it is successful installed\
yum repolist enabled| grep "mysql*"\
```
4.
```
#install mysql server via yum
yum install mysql-community-server
#Done!
```
5.
```
#start mysql server
systemctl start mysqld
systemctl status mysqld
```
6.
```
#default sql server port:  3306
```
# Can't find SOCKS when using pip
```
export all_proxy='https://<ip>:<port>'
```

# FAQ
1. Centos7 no models named '__sqlite3'?
> yum install sqlite-devel
rebuil python and install
2. How to use Choices's description in QuerySet object?
```html
video.get_definition_display
<!--definition is one field in the video-->
```
3. How to get duration of a video file?
use moviewpy in python
```
pip install moviepy
```
```python
#usage
from moviepy.editor import VideoFileClip
clip=VideoFileClip("myvideo.mp4")
print(clip.duration) #in seconds

```

4. Can't drop tables because of it contains foreign key.

Remove foreign key check and then can drop tables successfully!
```mysql
SET FOREIGN_KEY_CHECKS = 0;
drop table xxx;
```

5. Can't create table in an existing database.

Run in shell:
```
migrate --fake-initial <app_name> --database "<database_name_in_settings>"
```

6. Initiate data in database.

Use manage.py, run command:
```
manage.py loaddata <data_file_name>
```

the data file format is a json or yaml file.

# Useful 3rd-party app
## 1. Django Crispy Forms 
`pip install django-crispy-forms`
>settings.py
```
INSTALLED_APPS = {
...
'crispy_forms',
...
}
```
## 2. Django with Nginx-gunicorn

```shell
pip install gunicorn
gunicorn hello.wsgi:application --bind example.com:8001 #test gunicorn
```
```sehll
#edite file gunicorn_start, django.conf(for nginx)
./gunicorn_start
nginx -s reload
```

## Crispy Form Tags Settings
CRISPY_TEMPLATE_PACK = 'bootstrap3'
> *.html
```html
{% load crispy_forms_tags %}

<form method='POST' action='' >{%csrf_token%}
{{form|crispy}}
<input class='btn btn-primary' type='submit' value='Sign Up'/>
</form>
```
## 2. Django Registration Redux
https://django-registration-redux.readthedocs.io/en/latest/quickstart.html

`pip install django-registration-redux`
>settings.py
```
INSTALLED_APPS = {
...
'django.contrib.auth',
'django.contrib.sites',
'crispy_forms', 
...
}
#Django Registration Redux Settings
ACCOUNT_ACTIVATION_DAYS = 7 #days email is availd
REGISTRATION_AUTO_LOGIN = True
LOGIN_REDIRECT_URL='/'
```
>url.py
```
url(r'^accounts/',include('registration.backends.default.urls')),
```
>templets
>need to copy templates from official site

## 3. django-admin-resumable-js
awesome django admin resumable upload file app.
This Django-vod system customize it deeply to support dynamic upload path and multiple files upload.

## 4. Awesome Jquery Confirm Plugins
http://craftpip.github.io/jquery-confirm/


# TEMP
list all files in dir:
import os
for (dir,dirnames,filenames) in os.walk(MEDIA_ROOT,followlinks=True):
     for file in filenames:
             if file.endswith('mp4'):
                     print(dirnames,file)

# Versions
1. release1.0
...

2. release2.0
redesign file field, use more robost 3rd party app and deeply custmize it.Happy hacking!

# URLS
/       :   Home page
/vod    :   Django-vod
/replay :   Apache-tomcat:8080