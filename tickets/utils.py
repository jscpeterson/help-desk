from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.template.loader import render_to_string

from helpdesk import settings
from users.models import GROUP_SUPPORT, GROUP_SUPERVISOR


def send_resolution_email(ticket):

    context = {
        'recipient': ticket.user,
        'ticket_num': ticket.id,
        'assignee': ticket.assignee,
        'problem_description': ticket.problem_description,
        'resolution': ticket.resolution,
    }

    message = """
    Ticket #{{ ticket_num }} has been resolved by {{ assignee }}.

    Your issue was as follows: {{ problem_description }}

    {{ assignee }} provided this information with the resolution: {{ resolution }}
    """.format(context)

    html_message = render_to_string('emails/ticket_resolved.html', context)

    send_mail(
        subject='Help Desk Ticket #{} Resolved'.format(ticket.id),
        message=message,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[ticket.user.email],
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
