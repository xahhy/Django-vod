from django.contrib import admin
# Register your models here.
from .models import *
from django import forms
from django.contrib import messages
from uuslug import uuslug
from django.conf import settings
from .utils import *
import re

from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy


class VodForm(forms.ModelForm):
    """docstring for VodForm"""

    def __init__(self, *args, **kwargs):
        super(VodForm, self).__init__(*args, **kwargs)
        if (self.instance.image.name is '' or self.instance.image.name is None) \
                and (self.instance.video.name is '' or self.instance.video.name is None):
            print("save path is empty")
            self.fields["save_path"] = forms.ChoiceField(choices=save_path_choices())
        else:
            print("save path is:",self.instance.save_path)
            self.fields["save_path"] = forms.ChoiceField(choices=get_save_path_choice(self.instance.save_path))
            # self.fields['save_path'].widget.attrs['disabled="disabled"'] = True
        for instance in self.fields["category"].queryset:
            create_category_path(name=instance.name)

    def clean_title(self):
        print("vod form clean")
        data = self.cleaned_data['title']
        return data

    def clean(self):
        print("vod form clean all")
        return super(VodForm, self).clean()

    class Meta:
        model = Vod
        fields = '__all__'


class VodModelAdmin(admin.ModelAdmin):
    list_display = ["title", "image_tag", "category", "file_size", "duration", "definition", "year",
                    "view_count", "timestamp"]  # image_tag
    list_display_links = ["image_tag", "timestamp"]  # image_tag
    list_editable = ["category", 'title', "definition", "year"]
    list_filter = ["year", "category"]
    # fields = ('image_tag',)
    # readonly_fields = ('image_tag',)
    search_fields = ["title", "description"]
    actions = ["delete_hard", "copy_objects", "clear_view_count"]
    form = VodForm

    change_form_template = 'vodmanagement/change_form.html'
    add_form_template = 'vodmanagement/change_form.html'
    # def get_form(self, request, *args, **kwargs):
    #     form = super(VodModelAdmin, self).get_form(request, *args, **kwargs)
    #     form.base_fields['creator'].initial = request.user
    #     return form
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super(VodModelAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, object):
        try:
            delete_hard(object.image.path)
        except:
            pass
        try:
            delete_hard(object.video.path)
        except:
            pass
        object.delete()

    def delete_hard(self, request, queryset):
        for obj in queryset:
            try:
                delete_hard(obj.image.path)
            except:
                pass
            try:
                delete_hard(obj.video.path)
            except:
                pass
            obj.delete()

    delete_hard.short_description = "Delete  object from disk"

    def copy_objects(self, request, queryset):
        for obj in queryset:
            for i in range(4):
                new_obj = obj
                new_obj.pk = None
                # new_obj.slug = create_slug(new_obj)
                new_obj.slug = uuslug(new_obj.title, instance=new_obj)
                new_obj.save()
        self.message_user(request, "%s item successfully copyed." % queryset.count()
                          , messages.SUCCESS)

    def clear_view_count(self, request, queryset):
        queryset.update(view_count=0)
        self.message_user(request, "%s item successfully cleared view count." % queryset.count()
                          , messages.SUCCESS)

    class Media:
        pass
        # js = ("http://code.jquery.com/jquery.min.js",)

        # class Meta:
        # model = Vod


class MyAdminForm(forms.ModelForm):
    class Meta:
        model = VideoCategory
        widgets = {
            'type': forms.RadioSelect,
        }
        fields = '__all__'


class VideoCategoryModelAdmin(admin.ModelAdmin):
    list_display = ["category_description", "type", "isSecret"]
    list_editable = ["isSecret"]
    search_fields = ["name"]
    form = MyAdminForm

    def category_description(self, obj):
        return obj.name

    category_description.short_description = 'Category Name'


class LinkModelAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]
    list_editable = ["category"]


class MultipleUploadForm(forms.ModelForm):
    """docstring for VodForm"""

    def __init__(self, *args, **kwargs):
        super(MultipleUploadForm, self).__init__(*args, **kwargs)
        self.fields["save_path"] = forms.ChoiceField(choices=save_path_choices())

    class Meta:
        model = MultipleUpload
        fields = '__all__'


class MultipleUploadModelAdmin(admin.ModelAdmin):
    form = MultipleUploadForm
    change_form_template = 'vodmanagement/MultipleUpload/change_form.html'
    add_form_template = 'vodmanagement/MultipleUpload/change_form.html'


admin.site.register(FileDirectory)
admin.site.register(Link, LinkModelAdmin)
admin.site.register(VideoCategory, VideoCategoryModelAdmin)
admin.site.register(Vod, VodModelAdmin)
admin.site.register(UserPermission)
admin.site.register(MultipleUpload, MultipleUploadModelAdmin)
