from django.contrib import admin
# Register your models here.
from .models import *


class VodModelAdmin(admin.ModelAdmin):
    list_display = ["title","image_tag", "short_description","file_size","timestamp"]
    list_display_links = ["image_tag","title"]
    list_editable = []
    list_filter = ["timestamp"]
    # fields = ('image_tag',)
    # readonly_fields = ('image_tag',)
    search_fields = ["title", "content"]
    class Meta:
        model = Vod


class VideoCategoryModelAdmin(admin.ModelAdmin):
    list_display = ["category_description","type","directory","isSecret"]
    list_editable = ["isSecret"]
    search_fields = ["name"]

    def category_description(self,obj):
        return obj.name
    category_description.short_description = 'Category Name'


admin.site.register(FileDirectory)
admin.site.register(VideoCategory,VideoCategoryModelAdmin)
admin.site.register(Vod, VodModelAdmin)