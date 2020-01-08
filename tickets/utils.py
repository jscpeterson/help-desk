from django.core.mail import send_mail
from django.template.loader import render_to_string

from helpdesk import settings


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
