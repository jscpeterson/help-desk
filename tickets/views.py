from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from tickets.models import Ticket
from users.models import GROUP_SUPERVISOR, GROUP_SUPPORT, HelpDeskUser
from . import forms


@login_required
def home(request):
    if request.user.groups.filter(name=GROUP_SUPERVISOR).exists():
        return HttpResponseRedirect(reverse('tickets:view_unassigned_tickets'))
    elif request.user.groups.filter(name=GROUP_SUPPORT).exists():
        return HttpResponseRedirect(reverse('tickets:view_assigned_tickets'))
    else:
        return HttpResponseRedirect(reverse('tickets:view_user_tickets'))


@login_required
def view_user_tickets(request):
    template = 'tickets/view_user_tickets.html'
    context = {
        'first_name': request.user.first_name,
        'open_tickets': Ticket.objects.filter(user=request.user, status=Ticket.OPEN),
        'closed_tickets': Ticket.objects.filter(user=request.user, status=Ticket.CLOSED),
    }
    # TODO Order tickets by datetimes

    return render(request, template, context)


@login_required
def new_ticket(request, *args, **kwargs):
    template = 'tickets/new_ticket.html'
    if request.method == 'POST':
        form = forms.NewTicketForm(request.POST, *args, **kwargs)
        if form.is_valid():
            ticket = Ticket.objects.create(
                user=request.user,
                problem_description=form.cleaned_data.get('problem_description')
            )
            return HttpResponseRedirect(reverse('tickets:home'))
    else:
        form = forms.NewTicketForm(*args, **kwargs)

    context = {'form': form}
    return render(request, template, context)


@login_required
def view_unassigned_tickets(request):
    template = 'tickets/view_unassigned_tickets.html'
    context = {
        'first_name': request.user.first_name,
        'unassigned_tickets': Ticket.objects.filter(status=Ticket.OPEN, assignee=None),
    }
    # TODO Order tickets by datetimes

    return render(request, template, context)


@login_required
def assign_ticket(request, *args, **kwargs):
    template = 'tickets/assign_ticket.html'
    ticket = get_object_or_404(Ticket, id=kwargs.get('ticket_id'))

    # TODO Check support or supervisor permission
    # TODO Pass user to check permission
    if request.method == 'POST':
        form = forms.AssignTicketForm(request.POST, *args, **kwargs)
        if form.is_valid():
            data = form.cleaned_data

            ticket.assignee = data.get('assignee')
            ticket.priority = data.get('priority')
            ticket.category = data.get('category')
            ticket.notes = data.get('notes')
            ticket.assignment_date = timezone.now()
            ticket.save()

            return HttpResponseRedirect(reverse('tickets:home'))

    else:
        form = forms.AssignTicketForm(*args, **kwargs)
        assignee_queryset = HelpDeskUser.objects.filter(groups__name__in=[GROUP_SUPPORT])
        priority_choices = list(Ticket.PRIORITY_CHOICES)
        category_choices = list(Ticket.CATEGORY_CHOICES)

    context = {
        'form': form,
        'support_agents': assignee_queryset,
        'category_choices': category_choices,
        'priority_choices': priority_choices
    }
    return render(request, template, context)


@login_required
def view_assigned_tickets(request):
    template = 'tickets/view_assigned_tickets.html'
    context = {
        'first_name': request.user.first_name,
        'assigned_tickets': Ticket.objects.filter(assignee=request.user, status=Ticket.OPEN),
    }
    # TODO Order tickets by priority and datetime

    return render(request, template, context)


@login_required
def resolve_ticket(request, *args, **kwargs):
    template = 'tickets/resolve_ticket.html'
    ticket = get_object_or_404(Ticket, id=kwargs.get('ticket_id'))

    # TODO Check support or supervisor permission
    if request.method == 'POST':
        form = forms.ResolveTicketForm(request.POST, *args, **kwargs)
        if form.is_valid():
            data = form.cleaned_data

            ticket.resolution = data.get('resolution')
            ticket.closed_date = timezone.now()
            ticket.status = Ticket.CLOSED
            ticket.save()

            return HttpResponseRedirect(reverse('tickets:home'))

    else:
        form = forms.ResolveTicketForm(*args, **kwargs)

    context = {'form': form}
    return render(request, template, context)
