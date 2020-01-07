from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from tickets.models import Ticket
from . import forms


@login_required
def home(request):
    # return render(request, 'tickets/debug.html', {'name': request.user.first_name})
    return HttpResponseRedirect(reverse('tickets:view_user_tickets'))


@login_required
def view_user_tickets(request):
    template = 'tickets/view_user_tickets.html'
    context = {
        'first_name': request.user.first_name,
        'open_tickets': Ticket.objects.filter(user=request.user, status=Ticket.OPEN),
        'closed_tickets': Ticket.objects.filter(user=request.user, status=Ticket.CLOSED),
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
        return HttpResponseRedirect(reverse('tickets:view_user_tickets'))
    else:
        form = forms.NewTicketForm(*args, **kwargs)

    context = {'form': form}
    return render(request, 'tickets/new_ticket.html', context)


@login_required
def view_unassigned_tickets(request):
    template = 'tickets/view_unassigned_tickets.html'
    context = {}

    return render(request, template, context)


@login_required
def assign_ticket(request):
    template = 'tickets/assign_ticket.html'
    context = {}

    return render(request, template, context)


@login_required
def view_assigned_tickets(request):
    template = 'tickets/view_assigned_ticket.html'
    context = {}

    return render(request, template, context)


@login_required
def resolve_ticket(request):
    template = 'tickets/resolve_ticket.html'
    context = {}

    return render(request, template, context)
