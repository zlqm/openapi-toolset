from django import forms

from .models import Doc


class DocForm(forms.ModelForm):
    version = forms.SlugField()
    path = forms.FileField()

    class Meta:
        model = Doc
        fields = ('version', 'path')
