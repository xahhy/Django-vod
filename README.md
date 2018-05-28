
# Django-Vod
该项目是一个在线视频点播网站的服务器后端实现。使用Django作为后端框架，主要通过定制Django提供的Admin页面进行后台数据管理。使用Django REST framework开发Web APIs。

# 安装步骤
使用Docker安装本服务

- docker pull [Repository URL]
- docker pull mysql:5.7
- 复制docker-compose.yml到/home/share/vod目录中
- 复制MySQL配置文件[mysqld.cnf](https://github.com/xjtutongshi/video_servers/blob/docker/vod_server/mysql/mysql.conf.d/mysqld.cnf)到/home/share/docker/mysql/mysql.conf.d目录中
- 修改mysqld.cnf中的必要配置

初次部署服务需要执行以下步骤：
> 初始化docker swarm 集群 `docker swarm init --advertise-addr <ip>`
> 
> 收集静态资源文件`docker run --rm -it -e DJANGO_DB_HOST=<ip> -e TSRTMP_DB_HOST=<ip> python manage.py collectstatic`
>
> 创建管理员帐号 `docker run --rm -it -e DJANGO_DB_HOST=<ip> -e TSRTMP_DB_HOST=<ip> python manage.py createsuperuser`
>
> 创建数据表 `docker run --rm -it -e DJANGO_DB_HOST=<ip> -e TSRTMP_DB_HOST=<ip> python init_database.py`
> 
> 创建运行需要挂载的目录 `mkdir -p /home/share/vod/media && mkdir -p /home/share/vod/static`

更新和运行服务程序需要执行以下步骤：
> 更新docker service信息： `cd /home/share/vod && docker stack deploy -c docker-compose.yml vod`

执行`docker service ls`观察运行情况,下面是运行成功后的状态:
```bash
ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
c4jn3qg471bf        vod_vod             replicated          3/3                 vod:latest          *:8000->8000/tcp
4fkup123mpzb        vod_vod_db          replicated          1/1                 mysql:5.7           *:3306->3306/tcp

```
# 网站后端主要功能

## 1. 点播（vodmanagement)

- 提供统一的界面实现对视频条目的增删改查，每个视频均拥有如下字段：
  - 名称
  - 封面图片文件
  - 视频文件
  - 视频简介（富文本）
  - 视频分类
  - 视频上传后存储位置
  - 视频列表（如一个电视剧条目下拥有更多的子视频，每个子视频结构相同）
  - 搜索字段（可以是一个列表，为搜索功能提供索引字段）
  - 创建日期
- 提供视频分类功能
  - 二级分类
- 提供获取视频列表以及视频详细信息的API
- 提供视频搜索API
- 提供视频文件的可靠上传功能
- 数据备份以及恢复功能

## 2. 录播(epg)

- 提供统一的界面查看已经录制节目的信息（录制节目信息由视频录制软件实现，不包括在本项目中）
- 将已录制节目复制到点播视频列表中

# 项目APP中的数据模型（Model）说明

## 1. 点播（vodmanagement）

- FileDirectory（文件存储路径）
  - **path**（上传文件存储路径，包含一个缺省值）
- VideoRegin（视频所属地区）
  - **name**（视频所属地区名字）
- VideoCategory（视频所属分类）
  - **name**（视频分类名称）
  - type（视频类型，包含Common和Special purpose）（用处不大，可能会考虑**弃用**）
  - isSecret（是否加密）（用处不大，可能会考虑**弃用**）
  - **level**（分类等级，强制在1级分类和2级分类中做选择）
  - **subset**（分类关系，指向自己的Model，如果 是1级分类的话会包含该1级分类下的所有2级分类）
- MultipleUpload（批量上传）
  - files（待上传文件）
  - save_path（保存路径，在FileDirectory中做选择）
  - category（该次上传的所有文件所属分类，在VideoCategory中做选择）
- Restore（视频导入）
  - **txt_file**（配置文件）
  - zip_file（视频压缩包）
  - save_path（保存路径）
- Record（录制视频转点播后的视频）
  - **title**（标题）
  - **image**（封面图片文件）
  - **video**（视频文件，m3u8文件）
  - **start_time**（节目起始时间）
  - **end_time**（节目结束时间）
  - **video_list**（节目列表，在电视剧时使用）
  - active（是否激活，激活后才会在用户界面中看到）
  - channel（所属频道名称）
  - progress（拷贝为点播节目时的拷贝进度）
  - **select_name**（作为电视剧中的某一集时所显示的名称）
  - **description**（简介）
- Vod（点播视频）
  - **title**（标题）
  - **image**（封面图片）
  - **video** （视频文件）
  - duration（视频时长）
  - local_video（使用本地文件作为视频文件，根据实际情况选择是否启用该功能）
  - **definition** （视频分辨率，包括：标清、高清、超高清）
  - **category** （视频所属分类）
  - **save_path** （保存路径，在FileDirectory中做选择）
  - **year** （视频年份）
  - **region** （视频地区）
  - file_size （视频文件大小）
  - view_count （视频访问次数）
  - creator （视频上传者）
  - **description** （视频简介，富文本）
  - **select_name** （视频作为视频列表中的某一集时所显示的名称）
  - updated （自动生成字段，视频更新时间）
  - timestamp （自动生成字段，视频条目创建时间）
  - slug （通过程序生成可以代表该视频条目的唯一英文缩写）
  - search_word （提供自定义视频特征字段，为视频搜索时提供索引）
  - **video_list** （视频列表）
  - active （是否激活）

###Use MySQL db

reference:
> www.centoscn.com/mysql/2016/0315/6844.html
1. ​
```
#install dependencies
yum search libaio\
yum install libaio\
```
2. ​
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
> rebuil python and install
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
## Django Crispy Forms 
`pip install django-crispy-forms`
>settings.py
```
INSTALLED_APPS = {
...
'crispy_forms',
...
}
```
## Django with Nginx-gunicorn

```shell
pip install gunicorn
gunicorn hello.wsgi:application --bind example.com:8001 #test gunicorn
```
```shell
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
## Django Registration Redux
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

## django-admin-resumable-js
awesome django admin resumable upload file app.
This Django-vod system customize it deeply to support dynamic upload path and multiple files upload.

## Awesome Jquery Confirm Plugins
http://craftpip.github.io/jquery-confirm/

## django-sortedm2m
Make ManyToManyField Sortable on admin site.

https://github.com/gregmuellegger/django-sortedm2m

model.ManyToManyField -> SortedManyToManyField

**Migrating a ManyToManyField to be a SortedManyToManyField**

If you are using Django's migration framework and want to change a ManyToManyField to be a SortedManyToManyField (or the other way around), you will find that a migration created by Django's makemigrations will not work as expected.

In order to migrate a ManyToManyField to a SortedManyToManyField, you change the field in your models to be a SortedManyToManyField as appropriate and create a new migration with manage.py makemigrations. Before applying it, edit the migration file and change in the operations list migrations.AlterField to **AlterSortedManyToManyField** (import it from sortedm2m.operations). This operation will take care of changing the intermediate tables, add the ordering field and fill in default values.

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

# VOD API Reference
## Get All Categories
*URL:* <ip>:<port>/api/category

*Example Response:*
```json
{
    "电影": [
        {
            "name": "动作片"
        },
        {
            "name": "冒险片"
        },
        {
            "name": "科幻片"
        },
        {
            "name": "历史片"
        }
    ],
    "电视剧": [
        {
            "name": "都市"
        },
        {
            "name": "言情"
        }
    ]
}
```