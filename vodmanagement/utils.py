import logging
import os
import re
import time
from pathlib import Path

import humanfriendly
import platform
from django.conf import settings


# generate choices depending on the folders in '/media/xjtu'
# return choices
def save_path_choices():
    if 'Windows' in platform.system():
        return (('default', settings.MEDIA_ROOT + '()'),)

    root_size = get_free_size(settings.MEDIA_ROOT)
    choices = (('default', settings.MEDIA_ROOT + '(' + root_size + ')'),)
    for folder in get_media_folder():
        media_size = get_free_size(folder)
        choices = choices + ((os.path.basename(folder), folder + '(' + media_size + ')'),)
    return choices


def get_save_path_choice(key):
    choices = save_path_choices()
    for choice in choices:
        if choice[0] == key:
            return (choice,)
    return 'default'


# get free size of the path in human readable
def get_free_size(path):
    root_vfs = os.statvfs(path)
    root_free = root_vfs.f_frsize * root_vfs.f_bfree  # free bytes
    size = humanfriendly.format_size(root_free)
    return size


# 返回所有 sys_media_root 目录下的所有文件夹的列表
def get_media_folder():
    folders = []
    try:
        folders = [str(item) for item in Path(settings.SYSTEM_MEDIA_ROOT).iterdir() if item.is_dir()]
    except Exception as e:
        logging.error("无法列出 SYSTEM_MEDIA_ROOT:%s 目录下的所有文件夹,请检查该目录是否存在" % settings.SYSTEM_MEDIA_ROOT)
    return folders


# 在Django的MEDIA文件夹下创建软链接，链接到SYSTEM_MEDIA_ROOT文件下的所有文件夹
def create_storage_paths():
    if 'Windows' in platform.system():
        return

    for folder in get_media_folder():
        create_symlink(folder, os.path.join(settings.MEDIA_ROOT, os.path.basename(folder)))


def create_symlink(src, dst):
    try:
        os.makedirs(src)
    except:
        pass
    try:
        os.symlink(src, dst)
    except:
        pass


# format time in seconds to xx:xx:xx
def time_format(seconds):
    hour = int(seconds / 3600)
    minute = int((seconds - 60 * hour) / 60)
    second = int(seconds % 60)

    hour = "00" + str(hour)
    minute = "00" + str(minute)
    second = "00" + str(second)
    time = "%s:%s:%s" % (hour[-2:], minute[-2:], second[-2:])
    return time


def get_vod_field_list(model, field, category):
    if category:
        queryset = model.objects.filter(category__subset__name=category).values_list(field).distinct().order_by(field)
    else:
        queryset = model.objects.values_list(field).distinct().order_by(field)
    return queryset


# delete all files related to the file
def delete_hard(file_path):
    dir = os.path.dirname(file_path)
    basename = os.path.basename(file_path)
    print("base name=", basename)
    for (dir, dirnames, files) in os.walk(dir):
        for file in files:
            if re.match(re.escape(basename) + '*', file):
                print("matched file:", file)
                os.remove(os.path.join(dir, file))


def func_time(func):
    def run_time(*args, **kwargs):
        start = time.clock()  # time.clock()第一次调用的时候返回的是程序运行的实际时间
        ret = func(*args, **kwargs)
        stop = time.clock()  # time.clock()第二次调用的时候返回的是第一次调用后，到这次调用的时间间隔
        print(func, 'run_time:', (stop - start))
        return ret

    return run_time


def try_or_error(func):
    def result(*args, **kwargs):
        ret = 'Error'
        try:
            ret = func(*args, **kwargs)
        except Exception as e:
            logging.exception('Field is not available')
        return ret

    return result
