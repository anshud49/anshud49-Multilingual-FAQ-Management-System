from django import forms
from .models import FAQ
from ckeditor.widgets import CKEditorWidget

class FAQForms(forms.ModelForm):
    answer = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model=FAQ
        fields='__all__'
        