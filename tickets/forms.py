from django import forms
from django.forms import Form, ModelForm
from django.db.models import Q

from tickets.models import Ticket, Note
from users.models import HelpDeskUser, GROUP_SUPPORT, GROUP_SUPERVISOR

EMPTY_CHOICE = '---------'


class NewTicketForm(Form):

    def __init__(self, *args, **kwargs):
        super(NewTicketForm, self).__init__(*args, **kwargs)
        self.fields['problem_description'] = forms.CharField()


class AssignTicketForm(Form):

    def __init__(self, *args, **kwargs):
        ticket = Ticket.objects.get(id=kwargs.pop('ticket_id'))
        user = kwargs.pop('user')
        super(AssignTicketForm, self).__init__(*args, **kwargs)

        if user.is_superuser or user.groups.filter(name=GROUP_SUPERVISOR).exists():
            # ASSIGNEES FOR SUPERVISOR SHOULD BE ALL SUPPORT AGENTS AND SUPERVISOR SELF
            assignee_queryset = HelpDeskUser.objects.filter(Q(groups__name__in=[GROUP_SUPPORT]) | Q(id=user.id))
            assignee_queryset = assignee_queryset.distinct()
        elif user.groups.filter(name=GROUP_SUPPORT).exists():
            assignee_queryset = HelpDeskUser.objects.filter(id=user.id)

        self.fields['assignee'] = forms.ModelChoiceField(
            queryset=assignee_queryset,
            initial="",
        )

        priority_choices = list(Ticket.PRIORITY_CHOICES)
        category_choices = list(Ticket.CATEGORY_CHOICES)

        self.fields['priority'] = forms.ChoiceField(
            choices=priority_choices,
        )

        self.fields['category'] = forms.ChoiceField(
            choices=category_choices,
        )

        self.fields['notes'] = forms.CharField(
            required=False
        )


class ResolveTicketForm(Form):

    def __init__(self, *args, **kwargs):
        ticket = Ticket.objects.get(id=kwargs.pop('ticket_id'))
        super(ResolveTicketForm, self).__init__(*args, **kwargs)

        self.fields['resolution'] = forms.CharField(
            required=False
        )


class NewNoteForm(ModelForm):

    class Meta:
        model = Note
        fields = ['text']  # TODO Add File
