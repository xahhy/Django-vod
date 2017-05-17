from django import forms


from .models import Vod


class VodForm(forms.ModelForm):
    
    class Meta:
        model = Vod
        fields = [
            "title",
            # "content",
            "image",
        ]