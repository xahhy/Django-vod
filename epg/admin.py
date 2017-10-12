from django.contrib import admin
from django.contrib import messages
from django import forms

from .models import *


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
    list_display = ['channel', 'title', 'start_time', 'end_time', 'url', 'finished']
    list_display_links = ['channel']
    list_filter = ['finished', 'channel']
    search_fields = ['channel', 'title', 'start_time']

    actions = ["add_to_record"]

    def add_to_record(self, request, queryset):
        for obj in queryset:
            new_record = Record(
                channel=obj.channel,
                start_time=obj.start_time,
                end_time=obj.end_time,
                url=obj.url,
                title=obj.title,
                finished=obj.finished,
                event_id=obj.event_id,
                category=Category.objects.first()
            ).save()
        self.message_user(request, "%s item successfully added to record." % queryset.count()
                          , messages.SUCCESS)


# class RecordInLine(admin.StackedInline):
#     model = Record
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    # records = forms.ModelMultipleChoiceField(queryset=Record.objects.all())
    records = forms.ModelMultipleChoiceField(queryset=Record.objects.all())

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['records'].initial = self.instance.record_set.all()

    def save(self, *args, **kwargs):
        # FIXME: 'commit' argument is not handled
        # TODO: Wrap reassignments into transaction
        # NOTE: Previously assigned Foos are silently reset
        instance = super(CategoryForm, self).save(commit=False)
        self.fields['records'].initial.update(category=None)
        self.cleaned_data['records'].update(category=instance)
        return instance

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    filter_horizontal = ['records']
    # inlines = [RecordInLine]
    # form = CategoryForm

@admin.register(Record)
class RecordModelAdmin(admin.ModelAdmin):
    list_display = ['channel', 'title', 'url']
    # list_editable = ['category']


# admin.site.register(Channel, ChannelModelAdmin)
# admin.site.register(Program, ProgramModelAdmin)
# admin.site.register(Category, CategoryModelAdmin)
# admin.site.register(Record, RecordModelAdmin)
