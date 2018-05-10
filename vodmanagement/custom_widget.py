from django import forms
from django.conf import settings


class KindEditor(forms.Textarea):
    class Media:
        js = (
            settings.STATIC_URL + 'kindeditor/kindeditor-all.js',
            settings.STATIC_URL + 'kindeditor/lang/zh-CN.js',
            settings.STATIC_URL + 'kindeditor/config.js'
        )
