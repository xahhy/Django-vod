from django import forms

from vodmanagement.custom_widget import KindEditor
from vodmanagement.models import MultipleUpload, Restore, VideoCategory, Vod
from vodmanagement.utils import save_path_choices, get_save_path_choice, create_storage_paths


class MultipleUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MultipleUploadForm, self).__init__(*args, **kwargs)
        self.fields['save_path'] = forms.ChoiceField(choices=save_path_choices())

    class Meta:
        model = MultipleUpload
        fields = '__all__'


class RestoreForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RestoreForm, self).__init__(*args, **kwargs)
        self.fields['save_path'] = forms.ChoiceField(choices=save_path_choices())

    class Meta:
        model = Restore
        fields = '__all__'


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = VideoCategory
        widgets = {
            'type': forms.RadioSelect,
        }
        fields = '__all__'


class VodForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VodForm, self).__init__(*args, **kwargs)
        if self.instance.image.name and self.instance.video.name:
            self.fields['save_path'] = forms.ChoiceField(choices=get_save_path_choice(self.instance.save_path))
        else:
            print('save path is empty')
            self.fields['save_path'] = forms.ChoiceField(choices=save_path_choices())
            # self.fields['save_path'].widget.attrs['disabled='disabled''] = True
        create_storage_paths()

    def clean_title(self):
        print('vod form clean')
        data = self.cleaned_data['title']
        return data

    def clean(self):
        print('vod form clean all')
        return super(VodForm, self).clean()

    class Meta:
        model = Vod
        fields = (
            'category',
            'save_path',
            'video',
            'title',
            'image',
            'year',
            'description',
            'slug',
            'search_word',
        )
        widgets = {
            'description': KindEditor(),
        }