from django import forms
from polls.models import Sentence


class HomeForm(forms.ModelForm):
    class Meta:
        model = Sentence
        fields = ['sen_text']