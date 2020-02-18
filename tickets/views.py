from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q

from datetime import date, datetime

from tickets.models import Ticket, Note, MoveRequestTicket, NewUserTicket
from tickets.utils import send_resolution_email, check_groups, check_is_assigned, check_ticket_unresolved, \
    check_ticket_unassigned, send_new_ticket_alert_email, send_ticket_assigned_email, check_is_assigned_or_user, \
    send_new_note_email, check_groups_or_is_user
from users.models import GROUP_SUPERVISOR, GROUP_SUPPORT, HelpDeskUser, GROUP_DIVISION_HEAD
from . import forms

# TODO Reorganize views similar to urls


@login_required
def home(request):
    # TODO Some code cleanup is needed here
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
            if Ticket.objects.last() is not None and \
                    Ticket.objects.last().problem_description == form.cleaned_data.get('problem_description') and \
                    Ticket.objects.last().user == request.user:
                # Catch if the user made a duplicate submission, prevent from creating a new object
                ticket = Ticket.objects.last()
                pass
            else:
                ticket = Ticket.objects.create(
                    user=request.user,
                    problem_description=form.cleaned_data.get('problem_description')
                )

                send_new_ticket_alert_email(ticket, request)

            return HttpResponseRedirect(reverse('tickets:view_ticket', kwargs={"ticket_id": ticket.id}))
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
            ticket.assignment_date = timezone.now()
            ticket.assigned_by = request.user
            ticket.save()

            send_ticket_assigned_email(ticket, request)

            return HttpResponseRedirect(reverse('tickets:home'))

    else:
        form = forms.AssignTicketForm(*args, **kwargs)

    assignee_choices = form.fields['assignee'].choices
    priority_choices = form.fields['priority'].choices
    category_choices = form.fields['category'].choices  # TODO Set if a MoveRequest or NewUser, lock

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

    ticket_id = kwargs.get('ticket_id')

    context = {
        'form': form,
        'ticket_id': ticket_id,
    }
    return render(request, template, context)


@login_required
def closed_tickets(request):
    """Retrieve the closed tickets for supervisor and support roles."""
    template = 'tickets/view_closed_tickets.html'

    check_groups(request.user, [GROUP_SUPERVISOR, GROUP_SUPPORT])

    all_closed_tickets = Ticket.objects.filter(status=Ticket.CLOSED).order_by('-created_date')
    user_closed_tickets = all_closed_tickets.filter(assignee=request.user).order_by('-created_date')

    all_tickets_paginator = Paginator(all_closed_tickets, 10)
    user_tickets_paginator = Paginator(user_closed_tickets, 10)

    # ACCOUNTING FOR THE MULTIPLE PAGINATION IN THIS VIEW
    # SETS A SESSION VARIABLE TO MAINTAIN THE PAGINATION PAGE FOR ALL TICKETS
    if 'all_closed_page' in request.session and not request.GET.get('all_closed_page'):
        all_tickets_page = request.session.get('all_closed_page')
    else:
        all_tickets_page = request.GET.get('all_closed_page')
        request.session['all_closed_page'] = all_tickets_page

    # ACCOUNTING FOR THE MULTIPLE PAGINATION IN THIS VIEW
    # SETS A SESSION VARIABLE TO MAINTAIN THE PAGINATION PAGE FOR USER TICKETS
    if 'user_closed_page' in request.session and not request.GET.get('user_closed_page'):
        user_tickets_page = request.session.get('user_closed_page')
    else:
        user_tickets_page = request.GET.get('user_closed_page')
        request.session['user_closed_page'] = user_tickets_page

    all_paged_tickets = all_tickets_paginator.get_page(all_tickets_page)
    user_paged_tickets = user_tickets_paginator.get_page(user_tickets_page)

    context = {
        'all_paged_tickets': all_paged_tickets,
        'user_paged_tickets': user_paged_tickets,
    }

    return render(request, template, context)


@login_required
def search_tickets(request, **kwargs):
    """Return the tickets search page."""
    template = 'tickets/search_tickets.html'

    check_groups(request.user, [GROUP_SUPERVISOR, GROUP_SUPPORT])

    # If the REFERER is a page other than the tickets
    # search page, don't do any extra work, and don't render the table
    # filled with all Ticket objects. Just render the search page.
    # If you clicked the search tickets link from nav bar and you were
    # already on the search tickets page, just render basic page, no search results.
    if request.META.get('HTTP_REFERER') is None \
            or request.path not in request.META.get('HTTP_REFERER') \
            or 'nav' in request.path:
        return render(request, template, {
            'assignee_choices': HelpDeskUser.objects.filter(groups__name__in=[GROUP_SUPPORT]),
            'priority_choices': Ticket.PRIORITY_CHOICES,
            'category_choices': Ticket.CATEGORY_CHOICES,
            'status_choices': Ticket.STATUS_CHOICES,
            'values': request.GET,
        })

    queryset_list = Ticket.objects.all()

    # Assignees
    if 'assignee' in request.GET:
        assignees = request.GET.getlist('assignee')
        queryset_list = queryset_list.filter(assignee_id__in=assignees)

    # Priority Levels
    if 'priority' in request.GET:
        priorities = request.GET.getlist('priority')
        queryset_list = queryset_list.filter(priority__in=priorities)

    # Categories
    if 'category' in request.GET:
        categories = request.GET.getlist('category')
        queryset_list = queryset_list.filter(category__in=categories)

    # Ticket status
    if 'status' in request.GET:
        status = request.GET['status']
        queryset_list = queryset_list.filter(status__in=status)

    # Ticket opened on or after
    if 'openStart' in request.GET:
        open_start = request.GET['openStart']
        if open_start == '':
            pass
        else:
            open_start_datetime = date.fromisoformat(open_start)
            queryset_list = queryset_list.filter(created_date__gte=open_start_datetime)

    # Ticket opened on or before
    if 'openEnd' in request.GET:
        open_end = request.GET['openEnd']
        if open_end == '':
            pass
        else:
            open_end_datetime = date.fromisoformat(open_end)
            open_end_datetime = datetime.combine(open_end_datetime, datetime.max.time())
            queryset_list = queryset_list.filter(created_date__lte=open_end_datetime)

    # Ticket assigned on or after
    if 'assignStart' in request.GET:
        assigned_start = request.GET['assignStart']
        if assigned_start == '':
            pass
        else:
            assigned_start_datetime = date.fromisoformat(assigned_start)
            queryset_list = queryset_list.filter(assignment_date__gte=assigned_start_datetime)

    # Ticket assigned on or before
    if 'assignEnd' in request.GET:
        assigned_end = request.GET['assignEnd']
        if assigned_end == '':
            pass
        else:
            assigned_end_datetime = date.fromisoformat(assigned_end)
            assigned_end_datetime = datetime.combine(assigned_end_datetime, datetime.max.time())
            queryset_list = queryset_list.filter(assignment_date__lte=assigned_end_datetime)

    # Ticket closed on or after
    if 'closeStart' in request.GET:
        closed_start = request.GET['closeStart']
        if closed_start == '':
            pass
        else:
            closed_start_datetime = date.fromisoformat(closed_start)
            queryset_list = queryset_list.filter(assignment_date__gte=closed_start_datetime)

    # Ticket closed on or before
    if 'closeEnd' in request.GET:
        closed_end = request.GET['closeEnd']
        if closed_end == '':
            pass
        else:
            closed_end_datetime = date.fromisoformat(closed_end)
            closed_end_datetime = datetime.combine(closed_end_datetime, datetime.max.time())
            queryset_list = queryset_list.filter(assignment_date__lte=closed_end_datetime)

    # Users and Keywords
    # OR filter when searching on Keywords AND Users fields
    # Queryset of all tickets with partial matches of keywords and or users.
    # Keywords and users are text input fields, so they will always be present
    if 'keywords' in request.GET and 'users' in request.GET:
        keywords = request.GET['keywords']
        users = request.GET['users']
        if keywords == '' and users == '':
            pass
        else:
            keywords = keywords.split()
            users = users.split()

            description_queries = [Q(problem_description__icontains=keyword) for keyword in keywords]
            notes_queries = [Q(notes__text__icontains=keyword) for keyword in keywords]
            resolution_queries = [Q(resolution__icontains=keyword) for keyword in keywords]

            user_queries = [Q(user__username__icontains=user) for user in users]

            queries = resolution_queries + notes_queries + description_queries + user_queries

            query = queries.pop()
            for item in queries:
                query |= item
            queryset_list = queryset_list.filter(query)

    assignee_choices = HelpDeskUser.objects.filter(groups__name__in=[GROUP_SUPPORT])
    priority_choices = Ticket.PRIORITY_CHOICES
    category_choices = Ticket.CATEGORY_CHOICES
    status_choices = Ticket.STATUS_CHOICES
    searched_context = 'searchTicketsWrapper'

    context = {
        'assignee_choices': assignee_choices,
        'priority_choices': priority_choices,
        'category_choices': category_choices,
        'status_choices': status_choices,
        'found_tickets': queryset_list,
        'values': request.GET,
        'searched_context': searched_context,
    }

    return render(request, template, context)


@login_required
def add_note(request, *args, **kwargs):
    template = 'tickets/new_note.html'
    ticket = get_object_or_404(Ticket, id=kwargs.get('ticket_id'))
    check_is_assigned_or_user(request.user, ticket)

    if request.method == 'POST':
        form = forms.NewNoteForm(request.POST)
        if form.is_valid():
            if Note.objects.last() is not None and \
                    Note.objects.last().text == form.cleaned_data.get('text') and \
                    Note.objects.last().user == request.user:
                # Catch if the user made a duplicate submission, prevent from creating a new object
                pass
            else:
                # commit=False means the form doesn't save at this time.
                # commit defaults to True which means it normally saves.
                note_instance = form.save(commit=False)
                note_instance.user = request.user
                note_instance.ticket = ticket
                note_instance.save()
                send_new_note_email(note_instance, request)
            return HttpResponseRedirect(reverse('tickets:view_ticket', kwargs={"ticket_id": ticket.id}))
    else:
        form = forms.NewNoteForm()

    context = {
        'form': form,
        'user': request.user,
        'ticket': ticket,
    }
    return render(request, template, context)


@login_required
def view_ticket(request, *args, **kwargs):
    ticket = get_object_or_404(Ticket, id=kwargs.get('ticket_id'))

    template = 'tickets/view_ticket.html'

    notes = Note.objects.filter(ticket__id=ticket.id)

    if ticket.assignee is None:
        check_groups_or_is_user(request.user, ticket, [GROUP_SUPERVISOR, GROUP_SUPPORT])
    else:
        check_is_assigned_or_user(request.user, ticket)

    context = {
        'ticket': ticket,
        'notes': notes,
    }

    return render(request, template, context)


@login_required
def move_request(request, *args, **kwargs):
    template = 'tickets/move_request.html'
    check_groups(request.user, [GROUP_SUPERVISOR, GROUP_DIVISION_HEAD])

    if request.method == 'POST':
        form = forms.MoveRequestForm(request.POST, *args, **kwargs)
        if form.is_valid():
            if MoveRequestTicket.objects.last() is not None and \
                    MoveRequestTicket.objects.last().old_room_number == form.cleaned_data.get('old_room_number') and \
                    MoveRequestTicket.objects.last().new_room_number == form.cleaned_data.get('new_room_number') and \
                    MoveRequestTicket.objects.last().user == request.user:
                # Catch if the user made a duplicate submission, prevent from creating a new object
                ticket = Ticket.objects.last()
                pass
            else:
                move_request_format = 'MOVE REQUEST - {scheduled_move_date}\n' \
                                      'OLD DIVISION: {old_division}\n' \
                                      'OLD LOCATION: ({old_building}) {old_room_number}\n' \
                                      'NEW DIVISION: {new_division}\n' \
                                      'NEW LOCATION: ({new_building}) {new_room_number}'

                ticket = form.save(commit=False)
                ticket.user = request.user
                ticket.category = Ticket.MOVE_REQUEST
                ticket.save()
                ticket.problem_description = move_request_format.format(
                    scheduled_move_date=ticket.scheduled_move_date.strftime('%m/%d/%Y'),
                    old_division=ticket.get_old_division_display(),
                    old_building=ticket.get_old_building_display(),
                    old_room_number=ticket.old_room_number,
                    new_division=ticket.get_new_division_display(),
                    new_building=ticket.get_new_building_display(),
                    new_room_number=ticket.new_room_number,
                )
                ticket.save()
                send_new_ticket_alert_email(ticket, request)

            return HttpResponseRedirect(reverse('tickets:view_ticket', kwargs={"ticket_id": ticket.id}))
    else:
        form = forms.MoveRequestForm(*args, **kwargs)

    context = {'form': form}
    return render(request, template, context)


@login_required
def new_user_request(request, *args, **kwargs):
    template = 'tickets/new_user_request.html'
    check_groups(request.user, [GROUP_SUPERVISOR, GROUP_DIVISION_HEAD])

    if request.method == 'POST':
        form = forms.NewUserRequestForm(request.POST, *args, **kwargs)
        if form.is_valid():
            if NewUserTicket.objects.last() is not None and \
                    NewUserTicket.objects.last().name == form.cleaned_data.get('name') and \
                    NewUserTicket.objects.last().user == request.user:
                # Catch if the user made a duplicate submission, prevent from creating a new object
                ticket = Ticket.objects.last()
                pass
            else:
                move_request_format = 'NEW USER - {name} ({job_title})\n' \
                                      'Starts {start_date}\n' \
                                      'DIVISION: {division}\n' \
                                      'LOCATION: ({building}) {room_number}\n' \
                                      'CMS Access: {cms_access}' \
                                      '{needs_computer}{needs_email_account}'

                ticket = form.save(commit=False)
                ticket.user = request.user
                ticket.category = Ticket.NEW_USER
                ticket.save()
                ticket.problem_description = move_request_format.format(
                    name=ticket.name,
                    job_title=ticket.get_job_title_display(),
                    start_date=ticket.start_date.strftime('%m/%d/%Y'),
                    division=ticket.get_division_display(),
                    building=ticket.get_building_display(),
                    room_number=ticket.room_number,
                    cms_access=ticket.get_cms_access_display(),
                    needs_computer=', needs computer' if ticket.needs_computer else '',
                    needs_email_account=', needs email account' if ticket.needs_email_account else '',
                )
                ticket.save()
                send_new_ticket_alert_email(ticket, request)

            return HttpResponseRedirect(reverse('tickets:view_ticket', kwargs={"ticket_id": ticket.id}))
    else:
        form = forms.NewUserRequestForm(*args, **kwargs)

    context = {'form': form}
    return render(request, template, context)
