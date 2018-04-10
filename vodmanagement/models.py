import json

import six
from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.conf import settings
import humanfriendly
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_init, post_save
from django.dispatch import receiver

from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.core.files import File
from sortedm2m.fields import SortedManyToManyField
from uuslug import uuslug
import os
from .utils import *
import datetime
# from moviepy.editor import VideoFileClip # get video duration
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField
from .my_storage import *
from admin_resumable.fields import ModelAdminResumableFileField, ModelAdminResumableImageField, \
    ModelAdminResumableMultiFileField, ModelAdminResumableRestoreFileField
from django.utils.encoding import uri_to_iri
from pathlib import Path
from django.core.management import call_command

# for pinyin search
from xpinyin import Pinyin

if six.PY3:
    from django.utils.encoding import smart_str
else:
    from django.utils.encoding import smart_unicode as smart_str
"""
Copy data in XXX model:
>>> 
from vodmanagement.models import *
objs=Vod.objects.all()
for i in range(0,10):
    newobj=objs[0]
    newobj.pk=None
    newobj.save()    
>>>
This script will copy 10 objs[0] in database
"""


class UserPermission(models.Model):
    user = models.OneToOneField(User)
    permission = models.CharField(max_length=100, blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def has_permision(self):
        delta = self.end_date.date() - datetime.date.today()
        print(delta.days)
        if delta.days >= 0:
            return True
        return False


class VodManager(models.Manager):
    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return super(VodManager, self)  # .filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    # filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, extension)
    VodModel = instance.__class__
    print('save')
    if VodModel.objects.count() is not 0:
        new_id = VodModel.objects.order_by("id").last().id - 1
    else:
        new_id = 0
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    print('save image')
    return "%s/%s" % (new_id, filename)


def upload_video_location(instance, filename):
    VodModel = instance.__class__
    if VodModel.objects.count() is not 0:
        new_id = VodModel.objects.order_by("id").last().id + 1
    else:
        new_id = 0
    folder = instance.save_path
    if folder == "default":
        category = instance.category.name
    else:
        category = instance.category.name + '_' + folder
    print("video path:", category)
    return "%s/videos/%s/%s" % (category, new_id, filename)


def upload_image_location(instance, filename):
    VodModel = instance.__class__
    if VodModel.objects.count() is not 0:
        new_id = VodModel.objects.order_by("id").last().id + 1
    else:
        new_id = 0
    folder = instance.save_path
    if folder == "default":
        category = instance.category.name
    else:
        category = instance.category.name + '_' + folder
    return "%s/images/%s/%s" % (category, new_id, filename)


def upload_record_image_location(instance, filename):
    return "%s/images/%s" % (settings.RECORD_MEDIA_FOLDER, filename)


def default_description(instance):
    default = instance.title
    print(default)
    return 'The %s description' % default


# Create your models here.
def default_filedir():
    return settings.MEDIA_ROOT


# ---------------------------------------------------------------------
# if leave path blank,it will save it as the default file dir:settings.MEDIA_ROOT
class FileDirectory(models.Model):
    path = models.CharField(max_length=512, default=default_filedir, blank=True)

    class Meta:
        verbose_name = '视频上传路径'
        verbose_name_plural = '视频上传路径管理'

    def __str__(self):
        return self.path

    def save(self, *args, **kwargs):
        if self.path is None or self.path == "":
            self.path = default_filedir()
        super(FileDirectory, self).save(*args, **kwargs)


# ---------------------------------------------------------------------
# Two selections only:Common,Special purpose
TYPES = (
    ('common', 'Common'),
    ('special', 'Special purpose'),
)
VIDEO_QUALITY = [
    ('SD', '标清'),
    ('HD', '高清'),
    ('FHD', '超清'),
]
SAVE_PATH = (
    ('', settings.LOCAL_MEDIA_ROOT),
)


class VideoRegion(models.Model):
    name = models.CharField(max_length=200, verbose_name='地区', unique=True)

    class Meta:
        verbose_name = '视频地区管理'
        verbose_name_plural = '视频地区'

    def __str__(self):
        return self.name


class VideoCategory(models.Model):
    name = models.CharField(max_length=128, verbose_name='分类名称')
    type = models.CharField(max_length=128,
                            choices=TYPES,
                            default='common',
                            verbose_name='类型'
                            )
    isSecret = models.BooleanField(default=False, verbose_name='是否加密')
    level = models.IntegerField(null=False, blank=False, default=1, choices=((1, '一级分类'), (2, '二级分类')),
                                verbose_name='分类等级')
    subset = models.ManyToManyField('self', blank=True, verbose_name='分类关系')

    # directory = models.ForeignKey(FileDirectory)  # ,default=FileDirectory.objects.first())

    class Meta:
        verbose_name = '视频分类'
        # Edit Default Model Name for Human read
        verbose_name_plural = '视频分类管理'

    def __str__(self):
        base_name = self.name + str('  (level %d)' % (self.level))
        if self.subset.first() and self.level == 2:
            return '--'.join([self.subset.first().name, base_name])
        else:
            return base_name

    def save(self, *args, **kwargs):
        # print(self.directory)
        # make a folder self.name in the self.directory
        # src = self.directory.path+'/'+self.name
        # dst = settings.MEDIA_ROOT+'/'+str(self.name)
        # try:
        #     os.makedirs(src)
        # except:
        #     pass    
        # try:
        #     os.symlink(src,dst)
        # except:
        #     pass

        create_category_path(name=self.name)
        super(VideoCategory, self).save(*args, **kwargs)

    def colored_level(self):
        color_code = 'red' if self.level == 1 else 'green'
        return format_html(
            '<span style="color:{};">{}</span>',
            color_code,
            self.get_level_display()
        )

    colored_level.short_description = '分级'


# ---------------------------------------------------------------------
class MultipleUpload(models.Model):
    files = ModelAdminResumableMultiFileField(null=True, blank=True, storage=VodStorage())
    save_path = models.CharField(max_length=128, blank=False, null=True)
    category = models.ForeignKey(VideoCategory, null=True)

    class Meta:
        verbose_name = '批量上传'
        verbose_name_plural = '批量上传管理'


# ---------------------------------------------------------------------
# TODO(hhy): Please Leave This Model Here. It Will Be Use In The Future.
# class VideoTag(models.Model):
#     name = models.CharField(max_length=200, null=False, blank=False)
#
#     def __str__(self):
#         return self.name

# ---------------------------------------------------------------------
# TODO(hhy):Remove VodList Model. No Longer Used.
# class VodList(models.Model):
#     title = models.CharField(max_length=120)
#     image = ModelAdminResumableImageField(null=True, blank=True, storage=VodStorage(), verbose_name='缩略图')
#     description = models.TextField(blank=True)
#     category = models.ForeignKey(VideoCategory, null=True)
#     vod_list = models.ManyToManyField('Vod')
#     active = models.IntegerField(null=True, blank=False, default=0, choices=((1, 'Yes'), (0, 'No')))
#     tags = models.ManyToManyField(VideoTag, blank=True)
#
#     def colored_active(self):
#         color_code = 'red' if self.active == 0 else 'green'
#         return format_html(
#             '<span style="color:{};">{}</span>',
#             color_code,
#             self.get_active_display()
#         )
#     colored_active.short_description = '是否激活'
#
#     def __str__(self):
#         return self.title
# ---------------------------------------------------------------------
class Restore(models.Model):
    txt_file = models.FileField(blank=True, null=True, verbose_name='备份配置文件')
    zip_file = ModelAdminResumableRestoreFileField(null=True, blank=True, storage=VodStorage(), verbose_name='压缩包')
    save_path = models.CharField(max_length=128, blank=False, null=True)  # ,default=FileDirectory.objects.first())

    class Meta:
        verbose_name = '视频导入'
        verbose_name_plural = '视频导入'

    # @staticmethod
    # def parse_json(text):


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        result = super(Restore, self).save()
        file_path = self.txt_file.path
        call_command('loaddata', file_path)
        return result

# ---------------------------------------------------------------------

class Vod(models.Model):
    title = models.CharField(max_length=120, verbose_name='标题')
    # image = models.ImageField(upload_to=upload_image_location, null=True, blank=True)
    # video = models.FileField(upload_to=upload_video_location, null=True,blank=True,storage=VodStorage())
    image = ModelAdminResumableImageField(null=True, blank=True, storage=VodStorage(), verbose_name='缩略图')
    video = ModelAdminResumableFileField(null=True, blank=True, storage=VodStorage(), max_length=1000,
                                         verbose_name='视频')
    duration = models.CharField(max_length=50, blank=True, null=True, verbose_name='时长')
    local_video = models.FilePathField(path=settings.LOCAL_MEDIA_ROOT, blank=True, recursive=True)
    definition = models.CharField(max_length=10, choices=VIDEO_QUALITY, blank=False, default='H', verbose_name='清晰度')
    # image = FilerImageField(null=True, blank=True,
    #                         related_name="image_name")
    # video = FilerFileField(null=True, blank=True, related_name="video_name")
    # height_field = models.IntegerField(default=0)
    # width_field = models.IntegerField(default=0)
    category = models.ForeignKey(VideoCategory, null=True, verbose_name='分类')
    save_path = models.CharField(max_length=128, blank=False, null=True,
                                 default='default')  # ,default=FileDirectory.objects.first())
    year = models.CharField(max_length=10, blank=False, null=True,
                            default=datetime.datetime.now().year, verbose_name='年份')
    region = models.ForeignKey(VideoRegion, to_field='name', null=True, blank=True, on_delete=models.SET_NULL,
                               verbose_name='地区')
    file_size = models.CharField(max_length=128, default='0B', editable=False, verbose_name='文件大小')
    view_count = models.IntegerField(default=0, verbose_name='观看次数')
    view_count_temp = 0
    creator = models.ForeignKey(User, null=True, blank=False, editable=False)

    description = models.TextField(blank=True, verbose_name='简介')
    select_name = models.CharField(max_length=100, blank=False, verbose_name='选集名称', default='1')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='创建时间')  # The first time added
    slug = models.SlugField(unique=True, blank=True)
    search_word = models.CharField(max_length=10000, null=True, blank=True)
    # tags = models.ManyToManyField(VideoTag, blank=True)

    video_list = SortedManyToManyField('self', blank=True)
    # video_list = models.ManyToManyField('self', blank=True, symmetrical=False)
    active = models.IntegerField(null=True, blank=False, default=0, choices=((1, 'Yes'), (0, 'No')))
    progress = models.IntegerField(null=True, blank=True, default=0)
    objects = VodManager()

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = '视频列表'
        ordering = ["-timestamp", "-updated"]

    def save(self, without_valid=False, *args, **kwargs):
        print("------- save vod -------")
        p = Pinyin()
        full_pinyin = p.get_pinyin(smart_str(self.title), '')
        first_pinyin = p.get_initials(smart_str(self.title), '').lower()
        self.search_word = " ".join([full_pinyin, first_pinyin])
        print("video path:", self.video)

        if self.description is None or self.description == "":
            self.description = default_description(self)

        if self.local_video != '' and self.local_video is not None:
            basename = Path(self.local_video).relative_to(Path(settings.LOCAL_MEDIA_ROOT))
            self.video.name = str(Path(settings.LOCAL_MEDIA_URL) / basename)
            print("save local_video to filefield done")

        if without_valid:
            ret = super(Vod, self).save(*args, **kwargs)
            return ret
        super(Vod, self).save(*args, **kwargs)
        try:
            if self.video != None and self.video != '':
                relative_path = Path(self.video.name).relative_to(settings.MEDIA_URL)  # Djan%20go.mp4
                rel_name = uri_to_iri(relative_path)  # Djan go.mp4

                #  Make sure the self.video.name is not in the LOCAL_FOLDER
                if not self.video.name.startswith(settings.LOCAL_FOLDER_NAME) and \
                        not self.video.name.startswith(settings.RECORD_MEDIA_FOLDER):
                    self.video.name = str(rel_name)
                print("save_path:", self.save_path)
                print('video.name:', self.video.name)
                print('size:', self.video.file.size)
                self.file_size = humanfriendly.format_size(self.video.file.size)
                # duration = VideoFileClip(self.video.path).duration
                # self.duration = time_formate(duration)
                # print(self.duration)
            else:
                print("video file is None")
        except:
            pass

        try:
            if self.image:
                # self.image.name = os.path.join(self.save_path, os.path.basename(uri_to_iri(self.image.name)))
                self.image.name = str(uri_to_iri(Path(self.image.name).relative_to(settings.MEDIA_URL)))
        except:
            pass
        return super(Vod, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image is not None and str(self.image) != "":
            # print("image tage:"+str(self.image))
            if os.path.exists(self.image.path):
                return mark_safe('<img src="%s" width="150" height="200" />' % (self.image.url))
            else:
                return mark_safe('<img src="#" width="150" height="200" />')
        else:
            return mark_safe('<img src="%s" width="150" height="200" />' % (settings.DEFAULT_IMAGE_SRC))

    image_tag.short_description = '缩略图'

    def get_absolute_url(self):
        # print("get absolute url:",self.slug)
        return reverse("vod:vod-detail", kwargs={"slug": self.slug})

    def add_view_count(self):
        self.view_count_temp += 1

    def colored_active(self):
        color_code = 'red' if self.active == 0 else 'green'
        return format_html(
            '<span style="color:{};">{}</span>',
            color_code,
            self.get_active_display()
        )

    colored_active.short_description = '是否激活'


def create_slug(instance, new_slug=None, new_num=0):
    slug = slugify(instance.title)
    default_slug = slug
    if new_slug is not None:
        slug = new_slug
    qs = Vod.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_num += 1
        new_slug = "%s-%s" % (default_slug, new_num)
        return create_slug(instance, new_slug=new_slug, new_num=new_num)
    return slug


def slug_exists(slug):
    qs = Vod.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    return exists


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = uuslug(instance.title, instance=instance)
        # instance.slug = create_slug(instance)


def post_init_receiver(sender, instance, *args, **kwargs):
    # print("post_init!")
    pass


pre_save.connect(pre_save_post_receiver, sender=Vod)
post_init.connect(post_init_receiver, sender=Vod)
"""
from vodmanagement.models import *
objs = Vod.objects.all()
obj = objs.first()

"""
