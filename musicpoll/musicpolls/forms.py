from django import forms
from django.core.exceptions import ValidationError

from .models import Choice

class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
       # exclude = ["user"]

    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        super(ChoiceForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = HiddenInput()

    def clean(self):
        current_user = self.cleaned_data.get('user')
        current_index = self.cleaned_data.get('index')
        current_song = self.cleaned_data.get('song')
        print('por aqui no pasamos o que?:', current_user)
        user_choices = Choice.objects.filter(user=current_user)
        user_indexes = [choice.index for choice in user_choices]
        user_songs = [choice.song for choice in user_choices]
        if current_index in user_indexes:
            raise ValidationError("Index already used.")
        if current_song in user_songs:
            raise ValidationError("Song already voted.")
        return self.cleaned_data
