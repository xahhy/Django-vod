from pathlib import Path
from urllib import parse

import os
from django.contrib import admin
from django.contrib import messages
from django import forms

from mysite import settings
from vodmanagement.models import Record
from .models import *


# Custom Form

class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        wtf = Program.objects.filter(is_record=1)
        w = self.fields['records'].widget
        choices = []
        for choice in wtf:
            choices.append((choice.id, str(choice)))
        w.choices = choices


# Register your models here.
@admin.register(Channel)
class ChannelModelAdmin(admin.ModelAdmin):
    list_display = ['channel_id', 'channel_name', 'rtmp_url']
    list_display_links = ['channel_id']  # image_tag
    list_editable = ['channel_name', 'rtmp_url']
    search_fields = ['channel_id', 'channel_name']


@admin.register(Program)
class ProgramModelAdmin(admin.ModelAdmin):
    """
    Program admin site view
    """
    list_display = ['channel', 'title', 'start_time', 'end_time', 'url', 'finished', 'is_record']
    list_display_links = ['channel']
    list_filter = ['finished', 'channel']
    search_fields = ['channel', 'title', 'start_time']

    actions = ['record', 'unrecord']

    def record(self, request, queryset):
        # for obj in queryset:
        #     obj.is_record = 1
        #     obj.save()
        for program in queryset:
            m3u8_file_path = parse.urlparse(program.url).path
            m3u8_file_path = str(Path(settings.RECORD_MEDIA_ROOT) / Path(m3u8_file_path[1:]))
            print(m3u8_file_path)
            new_record = Record(title=program.title,
                                start_time=program.start_time,
                                end_time=program.end_time,
                                video=m3u8_file_path,
                                channel=program.channel)
            new_record.save()
        self.message_user(request, '%s 个节目被成功转成点播' % queryset.count()
                          , messages.SUCCESS)

    record.short_description = '转为点播'

    def unrecord(self, request, queryset):
        for obj in queryset:
            obj.is_record = 0
            obj.save()
        self.message_user(request, '%s 个节目被成功取消点播' % queryset.count()
                          , messages.SUCCESS)

    unrecord.short_description = '取消点播'


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    filter_horizontal = ['records']
    # inlines = [RecordInLine]
    form = CategoryForm

# admin.site.register(Channel, ChannelModelAdmin)
# admin.site.register(Program, ProgramModelAdmin)
# admin.site.register(Category, CategoryModelAdmin)
