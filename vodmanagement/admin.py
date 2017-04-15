from django.contrib import admin
# Register your models here.
from .models import *


class VodModelAdmin(admin.ModelAdmin):
    list_display = ["title","image_tag", "short_description","timestamp"]
    list_display_links = ["image_tag","title"]
    list_editable = []
    list_filter = ["timestamp"]
    # fields = ('image_tag',)
    # readonly_fields = ('image_tag',)
    search_fields = ["title", "content"]
    class Meta:
        model = Vod


class VideoCategoryTypeModelAdmin(admin.ModelAdmin):
    list_display = ("category_description")

    class Meta:
        model = VideoCategoryType

admin.site.register(VideoCategoryType)
admin.site.register(VideoCategory)
admin.site.register(Vod, VodModelAdmin)