from django import forms
from .models import Keyword, WhenEmail

class KeywordAddForm(forms.ModelForm):
  class Meta:
    model = Keyword
    fields = ('content',)

class WhenEmailAddForm(forms.ModelForm):
  class Meta:
    model = WhenEmail
    fields = ('date_email', 'date_reminder',)
