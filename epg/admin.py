from django.contrib import admin
from django.contrib import messages
from django import forms

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

    actions = ["chnage_for_record"]

    def chnage_for_record(self, request, queryset):
        for obj in queryset:
            obj.is_record = 1
            obj.save()
        self.message_user(request, "%s item successfully added to record." % queryset.count()
                          , messages.SUCCESS)


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    filter_horizontal = ['records']
    # inlines = [RecordInLine]
    form = CategoryForm



# admin.site.register(Channel, ChannelModelAdmin)
# admin.site.register(Program, ProgramModelAdmin)
# admin.site.register(Category, CategoryModelAdmin)
