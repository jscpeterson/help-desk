import os

from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string

from helpdesk.settings import base as settings
from tickets.models import Ticket
from users.models import GROUP_SUPPORT, GROUP_SUPERVISOR, HelpDeskUser

PLAINTEXT_MESSAGE = 'Please view this message in HTML rather than plaintext.'


def get_staff_emails():
    return [user.email for user in HelpDeskUser.objects.filter(groups__name__in=[GROUP_SUPPORT, GROUP_SUPERVISOR])]


def send_ticket_assigned_email(ticket, request):

    # Specify if a ticket was assigned to you by yourself or someone else
    assigner = request.user if ticket.assignee != request.user else 'yourself'

    context = {
        'recipient': ticket.assignee,
        'ticket': ticket,
        'assigner': assigner,
        'host': request.get_host(),
    }

    message = PLAINTEXT_MESSAGE

    # TODO Include category, priority, and notes in message (if they exist) (get_field_display not working correctly?)
    html_message = render_to_string('emails/ticket_assigned.html', context)

    send_mail(
        subject='You have been assigned Help Desk Ticket #{id}'.format(
            id=ticket.id,
        ),
        message=message,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[ticket.assignee.email],
        fail_silently=False,
    )


def send_new_ticket_alert_email(ticket, request):

    context = {
        'recipient': 'staff member',
        'ticket': ticket,
        'host': request.get_host()
    }

    message = PLAINTEXT_MESSAGE

    html_message = render_to_string('emails/new_ticket.html', context)

    send_mail(
        subject='New Help Desk Ticket #{id} from {user}'.format(id=ticket.id, user=ticket.user),
        message=message,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=get_staff_emails(),
        fail_silently=False,
    )


def send_resolution_email(ticket):
    context = {
        'recipient': ticket.user,
        'ticket': ticket,
    }

    message = PLAINTEXT_MESSAGE

    html_message = render_to_string('emails/ticket_resolved.html', context)

    send_mail(
        subject='Help Desk Ticket #{} Resolved'.format(ticket.id),
        message=message,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[ticket.user.email],
        fail_silently=False,
    )


def send_new_note_email(note, request):

    context = {
        'note': note,
        'host': request.get_host(),
    }

    # If there is no assignee, notify the user only. Unless the request.user is the user, in which case send no email.
    if note.ticket.assignee is None:
        if request.user == note.ticket.user:
            return
        context['recipient'] = note.ticket.user
        recipient_list = [note.ticket.user.email]
    # If the author of the note is the ticket assignee, notify the user
    elif note.user == note.ticket.assignee:
        context['recipient'] = note.ticket.user
        recipient_list = [note.ticket.user.email]
    # If the author of the note is the ticket user, notify the assignee
    elif note.user == note.ticket.user:
        context['recipient'] = note.ticket.assignee
        recipient_list = [note.ticket.assignee.email]
    # If the author of the note is not the assignee or the user but is a supervisor or superuser,
    # notify both the user and the assignee.
    elif note.user.is_superuser or note.user.is_supervisor():
        context['recipient'] = 'user'
        recipient_list = [note.ticket.user.email, note.ticket.assignee.email]
    else:
        # Something went wrong.
        raise Exception('New note added, author is not the assignee, user, or a superuser/supervisor.')

    message = PLAINTEXT_MESSAGE

    html_message = render_to_string('emails/new_note.html', context)

    send_mail(
        subject='Note posted on Help Desk Ticket #{}'.format(note.ticket.id),
        message=message,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
    )


def is_in_groups(user, group_names):
    """
    Returns True if the user is a member of any groups given their names in group_names
    """
    return any(user.groups.filter(name=group_name).exists() for group_name in group_names)


def check_groups(user, group_names):
    """
    Checks if the user is a superuser or in an allowed group for a given list of group names.
    Raises PermissionDenied exception if not.
    """
    if user.is_superuser or is_in_groups(user, group_names):
        return
    else:
        raise PermissionDenied()


def check_groups_or_is_user(user, ticket, group_names):
    """
    Checks if the user is a superuser or in an allowed group for a given list of group names, or if a
    ticket was submitted by the user.
    Raises PermissionDenied exception if not.
    """
    if user.is_superuser or is_in_groups(user, group_names) or user == ticket.user:
        return
    else:
        raise PermissionDenied()


def check_is_assigned(user, ticket):
    """
    Checks if user is a superuser/supervisor or if the user is a support user and is assigned to a ticket.
    Raises PermissionDenied exception if not.
    """
    if user.is_superuser or user.groups.filter(name=GROUP_SUPERVISOR).exists():
        return
    elif user.groups.filter(name=GROUP_SUPPORT).exists() and ticket.assignee == user:
        return
    else:
        raise PermissionDenied()


def check_is_assigned_or_user(user, ticket):
    """
    Checks if user is a superuser/supervisor or if the user is a support user and is assigned to a ticket,
    or if the ticket was submitted by the user.
    Raises PermissionDenied exception if not.
    """
    if user.is_superuser or user.groups.filter(name=GROUP_SUPERVISOR).exists():
        return
    elif user.groups.filter(name=GROUP_SUPPORT).exists() and ticket.assignee == user:
        return
    elif ticket.user == user:
        return
    else:
        raise PermissionDenied()


def check_ticket_unresolved(request, ticket):
    if ticket.status is Ticket.CLOSED:
        return render(request, 'errors/ticket_already_resolved.html', {'ticket_num': ticket.id})


def check_ticket_unassigned(request, ticket):
    if ticket.assignee is not None:
        return render(request, 'errors/ticket_already_assigned.html', {'ticket_num': ticket.id})
