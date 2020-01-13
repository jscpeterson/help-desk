from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from tickets.models import Ticket
from tickets.utils import send_resolution_email, check_groups, check_is_assigned, check_ticket_unresolved, \
    check_ticket_unassigned
from users.models import GROUP_SUPERVISOR, GROUP_SUPPORT, HelpDeskUser
from . import forms


@login_required
def home(request):

    welcomeMessage = messages.success(request, "Welcome")

    if request.user.groups.filter(name=GROUP_SUPERVISOR).exists():
        welcomeMessage
        return HttpResponseRedirect(reverse('tickets:view_unassigned_tickets'))
    elif request.user.groups.filter(name=GROUP_SUPPORT).exists():
        welcomeMessage
        return HttpResponseRedirect(reverse('tickets:view_assigned_tickets'))
    else:
        welcomeMessage
        return HttpResponseRedirect(reverse('tickets:view_user_tickets'))


@login_required
def view_user_tickets(request):

    template = 'tickets/view_user_tickets.html'
    context = {
        'first_name': request.user.first_name,
        'open_tickets': Ticket.objects.filter(user=request.user, status=Ticket.OPEN).order_by('created_date'),
        'closed_tickets': Ticket.objects.filter(user=request.user, status=Ticket.CLOSED).order_by('created_date'),
    }

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
        'unassigned_tickets': Ticket.objects.filter(status=Ticket.OPEN, assignee=None).order_by('created_date'),
        'assigned_tickets': Ticket.objects.filter(status=Ticket.OPEN).exclude(assignee=None).order_by('created_date')
        .order_by('priority'),
    }

    return render(request, template, context)


@login_required
def assign_ticket(request, *args, **kwargs):
    ticket = get_object_or_404(Ticket, id=kwargs.get('ticket_id'))

    check_groups(request.user, [GROUP_SUPERVISOR, GROUP_SUPPORT])

    if ticket.status is Ticket.CLOSED:
        return render(request, 'errors/ticket_already_resolved.html', {'ticket_num': ticket.id})
    if ticket.assignee is not None:
        return render(request, 'errors/ticket_already_assigned.html', {'ticket_num': ticket.id})

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

    assignee_choices = form.fields['assignee'].choices
    priority_choices = form.fields['priority'].choices
    category_choices = form.fields['category'].choices

    context = {
        'form': form,
        'support_agents': assignee_choices,
        'category_choices': category_choices,
        'priority_choices': priority_choices
    }
    return render(request, template, context)


@login_required
def view_assigned_tickets(request):
    check_groups(request.user, [GROUP_SUPERVISOR, GROUP_SUPPORT])

    template = 'tickets/view_assigned_tickets.html'
    context = {
        'first_name': request.user.first_name,
        'assigned_tickets': Ticket.objects.filter(assignee=request.user, status=Ticket.OPEN).order_by('created_date')
        .order_by('priority'),
        'unassigned_tickets': Ticket.objects.filter(status=Ticket.OPEN, assignee=None).order_by('created_date'),
    }

    return render(request, template, context)


@login_required
def resolve_ticket(request, *args, **kwargs):
    ticket = get_object_or_404(Ticket, id=kwargs.get('ticket_id'))

    check_groups(request.user, [GROUP_SUPERVISOR, GROUP_SUPPORT])

    if ticket.status is Ticket.CLOSED:
        return render(request, 'errors/ticket_already_resolved.html', {'ticket_num': ticket.id})

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


@login_required
def closed_tickets(request):
    """Retrieve the closed tickets for supervisor and support roles."""
    template = 'tickets/view_closed_tickets.html'

    check_groups(request.user, [GROUP_SUPERVISOR, GROUP_SUPPORT])

    all_closed_tickets = Ticket.objects.filter(status=Ticket.CLOSED)
    user_closed_tickets = all_closed_tickets.filter(assignee=request.user)

    context = {
        'all_closed_tickets': all_closed_tickets.order_by('created_date'),
        'user_closed_tickets': user_closed_tickets.order_by('created_date'),
    }

    return render(request, template, context)
