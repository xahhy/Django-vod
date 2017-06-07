import os
from django.conf import settings
import humanfriendly
from vodmanagement.models import *

sys_media_root = '/media/xjtu'

# generate choices depending on the folders in '/media/xjtu'
# return choices
def save_path_choices():
    root_size = get_free_size(settings.MEDIA_ROOT)
    choices=(('default',settings.MEDIA_ROOT+'('+root_size+')'),)
    for folder in get_media_folder():
        media_size = get_free_size(folder)
        choices = choices + ((os.path.basename(folder),folder+'('+media_size+')'),)

    return choices

# get free size of the path in human readable
def get_free_size(path):
    root_vfs = os.statvfs(path)
    root_free = root_vfs.f_frsize * root_vfs.f_bfree # free bytes
    size = humanfriendly.format_size(root_free)
    return size

# get folders in sys_media_root
# return a list
def get_media_folder():
    folders=[]
    for item in os.listdir(sys_media_root):
        real_path = sys_media_root+'/'+item
        if os.path.isdir(real_path):
            folders.append(real_path)

    return folders

# if name="Action", a folder named "USB" in the sys_media_root ,
# it will create a real folder named "Action_USB" in the USB folder
def create_category_path(name):
    for folder in get_media_folder():
        print(folder,name)
        new_name = name+'_'+os.path.basename(folder)
        create_symlink(folder, settings.MEDIA_ROOT, new_name)
 
def create_symlink(src,dst,name):
    src += '/'+ name
    dst += '/'+ name
    try:
        os.makedirs(src)
    except:
        pass    
    try:
        os.symlink(src,dst)
    except:
        pass

def time_formate(seconds):
    hour    = int(seconds/3600)
    minute  = int((seconds-60*hour)/60) 
    second  = int(seconds%60)

    hour    = "00"+str(hour)
    minute    = "00"+str(minute)
    second    = "00"+str(second)
    time = "%s:%s:%s"%(hour[-2:],minute[-2:],second[-2:])
    return time


