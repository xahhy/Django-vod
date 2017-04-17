from django.contrib import admin
# Register your models here.
from .models import *
from django import forms

class VodModelAdmin(admin.ModelAdmin):
    list_display = ["title","image_tag", "short_description","file_size","creator","timestamp"]
    list_display_links = ["image_tag","title"]
    list_editable = []
    list_filter = ["timestamp"]
    # fields = ('image_tag',)
    # readonly_fields = ('image_tag',)
    search_fields = ["title", "content"]

    # def get_form(self, request, *args, **kwargs):
    #     form = super(VodModelAdmin, self).get_form(request, *args, **kwargs)
    #     form.base_fields['creator'].initial = request.user
    #     return form
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super(VodModelAdmin, self).save_model(request, obj, form, change)

    class Meta:
        model = Vod


class MyAdminForm(forms.ModelForm):
  class Meta:
    model = VideoCategory
    widgets = {
      'type': forms.RadioSelect,
    }
    fields = '__all__'


class VideoCategoryModelAdmin(admin.ModelAdmin):
    list_display = ["category_description","type","directory","isSecret"]
    list_editable = ["isSecret"]
    search_fields = ["name"]
    form = MyAdminForm

    def category_description(self,obj):
        return obj.name
    category_description.short_description = 'Category Name'



admin.site.register(FileDirectory)
admin.site.register(Link)
admin.site.register(VideoCategory,VideoCategoryModelAdmin)
admin.site.register(Vod, VodModelAdmin)