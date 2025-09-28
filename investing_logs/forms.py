from django import forms
from .models import Instrument,Entry


class InstrumentForm(forms.ModelForm):
    class Meta:
        model = Instrument
        fields = ['text']
        labels = {'text': ''}



class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}