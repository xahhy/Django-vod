from django.contrib import admin
# Register your models here.
from .models import *
from django import forms
from django.contrib import messages


class VodModelAdmin(admin.ModelAdmin):
    list_display = ["title","image_tag","category","file_size","creator", "definition","view_count"] #image_tag
    list_display_links = ["image_tag",]#image_tag
    list_editable = ["category", 'title', "definition"]
    list_filter = ["timestamp","category"]
    # fields = ('image_tag',)
    # readonly_fields = ('image_tag',)
    search_fields = ["title", "description"]
    actions = ["delete_hard", "copy_objects", "clear_view_count"]
    # def get_form(self, request, *args, **kwargs):
    #     form = super(VodModelAdmin, self).get_form(request, *args, **kwargs)
    #     form.base_fields['creator'].initial = request.user
    #     return form
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super(VodModelAdmin, self).save_model(request, obj, form, change)

    def delete_hard(self, request, queryset):
        for obj in queryset:
            try:
                # print(obj.image.file.)
                os.remove(obj.image.path)
                os.remove(obj.video.path)
                pass
            except:
                pass 

            obj.delete()
    delete_hard.short_description = "Delete  object from disk"

    def copy_objects(self,request,queryset):
        for obj in queryset:
            new_obj = obj
            new_obj.pk = None
            new_obj.slug = create_slug(new_obj)
            new_obj.save()
        self.message_user(request,"%s item successfully copyed."%queryset.count()
            ,messages.SUCCESS)

    def clear_view_count(self,request,queryset):
        queryset.update(view_count=0)
        self.message_user(request,"%s item successfully cleared view count."%queryset.count()
            ,messages.SUCCESS)

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

class LinkModelAdmin(admin.ModelAdmin):
    list_display = ["name","category"]
    list_editable = ["category"]

admin.site.register(FileDirectory)
admin.site.register(Link,LinkModelAdmin)
admin.site.register(VideoCategory,VideoCategoryModelAdmin)
admin.site.register(Vod, VodModelAdmin)