from django import forms
from django.forms import Form

from tickets.models import Ticket
from users.models import HelpDeskUser, GROUP_SUPPORT, GROUP_SUPERVISOR

EMPTY_CHOICE = '---------'


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
        user = kwargs.pop('user')
        super(AssignTicketForm, self).__init__(*args, **kwargs)

        if user.is_superuser or user.groups.filter(name=GROUP_SUPERVISOR).exists():
            assignee_queryset = HelpDeskUser.objects.filter(groups__name__in=[GROUP_SUPPORT])
        elif user.groups.filter(name=GROUP_SUPPORT).exists():
            assignee_queryset = HelpDeskUser.objects.filter(id=user.id)

        self.fields['assignee'] = forms.ModelChoiceField(
            queryset=assignee_queryset,
            label='Assign this task to a support agent:',
            required=True,
        )

        priority_choices_with_empty = [('', EMPTY_CHOICE)] + list(Ticket.PRIORITY_CHOICES)
        category_choices_with_empty = [('', EMPTY_CHOICE)] + list(Ticket.CATEGORY_CHOICES)

        self.fields['priority'] = forms.ChoiceField(
            choices=priority_choices_with_empty,
            label='Assign a priority level:',
            required=True,
        )

        self.fields['category'] = forms.ChoiceField(
            choices=category_choices_with_empty,
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