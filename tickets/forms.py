from django import forms
from django.forms import Form


class NewTicketForm(Form):

    def __init__(self, *args, **kwargs):
        super(NewTicketForm, self).__init__(*args, **kwargs)
        self.fields['problem_description'] = forms.CharField(
            widget=forms.Textarea,
            label='Please describe your problem.',
            required=True,
        )
