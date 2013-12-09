from django.forms import ModelForm, IntegerField
from django.core.exceptions import ValidationError
from django.forms.widgets import HiddenInput
from django.contrib.auth.models import User

from .models import Choice, Song

class AddSongForm(ModelForm):
    pk = IntegerField(required=False)

    class Meta:
        model = Song

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('requestuser')
        super(AddSongForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = HiddenInput()
        self.fields['artist'].widget = HiddenInput()
        self.fields['lasturl'].widget = HiddenInput()
        self.fields['photourl'].widget = HiddenInput()
        self.fields['pk'].widget = HiddenInput()

    def clean(self):
        lasturl = self.cleaned_data.get('lasturl')
        pk = self.cleaned_data.get('pk')
        lasturl_in_songs = Song.objects.filter(lasturl=lasturl)
        if not pk and lasturl_in_songs:
            raise ValidationError("Song already in database.")
        if pk:
            current_song = Song.objects.get(id=pk)
            user_choices = Choice.objects.filter(user=self.user)
            user_songs = [choice.song for choice in user_choices]
            if current_song in user_songs:
                raise ValidationError("Song already voted.")
        return self.cleaned_data


class ChoiceDeleteForm(ModelForm):

    class Meta:
        model = Choice


class ChoiceForm(ModelForm):

    class Meta:
        model = Choice

    def __init__(self, *args, **kwargs):
        super(ChoiceForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = HiddenInput()

    def clean(self):
        current_user = self.cleaned_data.get('user')
        current_index = self.cleaned_data.get('index')
        current_song = self.cleaned_data.get('song')
        user_choices = Choice.objects.filter(user=current_user)
        user_indexes = [choice.index for choice in user_choices]
        user_songs = [choice.song for choice in user_choices]
        if current_index in user_indexes:
            raise ValidationError("Index already used.")
        if current_song in user_songs:
            raise ValidationError("Song already voted.")
        return self.cleaned_data
