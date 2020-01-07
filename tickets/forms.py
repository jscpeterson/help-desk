from django import forms
from django.forms import Form

from tickets.models import Ticket
from users.models import HelpDeskUser, GROUP_SUPPORT


class NewTicketForm(Form):

    def __init__(self, *args, **kwargs):
        super(NewTicketForm, self).__init__(*args, **kwargs)
        self.fields['problem_description'] = forms.CharField(
            widget=forms.Textarea,
            label='Please describe your problem.',
            required=True,
        )


class AssignTicketForm(Form):

    def __init__(self, *args, **kwargs):
        ticket = Ticket.objects.get(id=kwargs.pop('ticket_id'))
        super(AssignTicketForm, self).__init__(*args, **kwargs)

        # TODO If the user is SUPPORT and not SUPERVISOR, make the only choice themself
        assignee_queryset = HelpDeskUser.objects.filter(groups__name__in=[GROUP_SUPPORT])
        self.fields['assignee'] = forms.ModelChoiceField(
            queryset=assignee_queryset,
            label='Assign this task to a support agent:',
            required=True,
        )

        self.fields['priority'] = forms.ChoiceField(
            choices=Ticket.PRIORITY_CHOICES,
            label='Assign a priority level:',
            required=True,
        )

        self.fields['category'] = forms.ChoiceField(
            choices=Ticket.CATEGORY_CHOICES,
            label='Assign a category:',
            required=True,
        )

        self.fields['notes'] = forms.CharField(
            widget=forms.Textarea,
            label='Notes:',
            required=False,
        )


class ResolveTicketForm(Form):

    def __init__(self, *args, **kwargs):
        ticket = Ticket.objects.get(id=kwargs.pop('ticket_id'))
        super(ResolveTicketForm, self).__init__(*args, **kwargs)

        self.fields['resolution'] = forms.CharField(
            widget=forms.Textarea,
            label='Resolution Notes:',
            required=False,
        )
