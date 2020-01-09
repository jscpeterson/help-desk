from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from tickets.models import Ticket
from tickets.utils import send_resolution_email
from users.models import GROUP_SUPERVISOR, GROUP_SUPPORT
from . import forms


def check_groups(user, group_names):
    """
    Checks if the user is a superuser or in an allowed group for a given list of group names.
    Raises PermissionDenied exception if not.
    """
    if user.is_superuser or any(user.groups.filter(name=group_name).exists() for group_name in group_names):
        return True
    else:
        raise PermissionDenied()


def check_is_assigned(user, ticket):
    """
    Checks if user is a superuser/supervisor or if the user is a support user and is assigned to a ticket.
    Raises PermissionDenied exception if not.
    """
    if user.is_superuser or user.groups.filter(name=GROUP_SUPERVISOR).exists():
        return True
    elif user.groups.filter(name=GROUP_SUPPORT).exists() and ticket.assignee == user:
        return True
    else:
        raise PermissionDenied()


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
    check_groups(request.user, [GROUP_SUPERVISOR, GROUP_SUPPORT])

    template = 'tickets/view_unassigned_tickets.html'
    context = {
        'first_name': request.user.first_name,
        'unassigned_tickets': Ticket.objects.filter(status=Ticket.OPEN, assignee=None),
    }
    # TODO Order tickets by datetimes

    return render(request, template, context)


@login_required
def assign_ticket(request, *args, **kwargs):
    ticket = get_object_or_404(Ticket, id=kwargs.get('ticket_id'))
    check_groups(request.user, [GROUP_SUPERVISOR, GROUP_SUPPORT])

    template = 'tickets/assign_ticket.html'
    kwargs['user'] = request.user

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

    context = {'form': form}
    return render(request, template, context)


@login_required
def view_assigned_tickets(request):
    check_groups(request.user, [GROUP_SUPERVISOR, GROUP_SUPPORT])

    template = 'tickets/view_assigned_tickets.html'
    context = {
        'first_name': request.user.first_name,
        'assigned_tickets': Ticket.objects.filter(assignee=request.user, status=Ticket.OPEN),
    }
    # TODO Order tickets by priority and datetime

    return render(request, template, context)


@login_required
def resolve_ticket(request, *args, **kwargs):
    ticket = get_object_or_404(Ticket, id=kwargs.get('ticket_id'))
    check_is_assigned(request.user, ticket)

    template = 'tickets/resolve_ticket.html'

    if request.method == 'POST':
        form = forms.ResolveTicketForm(request.POST, *args, **kwargs)
        if form.is_valid():
            data = form.cleaned_data

            ticket.resolution = data.get('resolution')
            ticket.closed_date = timezone.now()
            ticket.status = Ticket.CLOSED
            ticket.save()

            send_resolution_email(ticket)

            return HttpResponseRedirect(reverse('tickets:home'))

    else:
        form = forms.ResolveTicketForm(*args, **kwargs)

    context = {'form': form}
    return render(request, template, context)
