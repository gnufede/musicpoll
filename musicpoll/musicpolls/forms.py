from django import forms
from django.core.exceptions import ValidationError

from .models import Choice

class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice

    def clean(self):
        current_user = (self.cleaned_data.get('user')
        current_index = (self.cleaned_data.get('index')
        last_choice = Choice.objects.filter(user=current_user,
                                            index=current_index)
        if last_choice:
            raise ValidationError(
                    "Index already used."
                    )
        return self.cleaned_data
