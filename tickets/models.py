from django.db import models

from users.models import HelpDeskUser


class Ticket(models.Model):

    user = models.ForeignKey(
        HelpDeskUser,
        related_name='submitted_tickets',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    # Automatically created
    created_date = models.DateTimeField(
        auto_now_add=True
    )

    # To be added by the user
    problem_description = models.TextField(
        default=''
    )

    # To be assigned by a supervisor
    assignee = models.ForeignKey(
        HelpDeskUser,
        related_name='assigned_tickets',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    # Supervisor that assigned this ticket
    assigned_by = models.ForeignKey(
        HelpDeskUser,
        related_name='tickets_assigned_by',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    HIGH_PRIORITY = 1
    NORMAL_PRIORITY = 2
    LOW_PRIORITY = 3

    PRIORITY_CHOICES = (
        (HIGH_PRIORITY, 'High'),
        (NORMAL_PRIORITY, 'Normal'),
        (LOW_PRIORITY, 'Low'),
    )

    # To be assigned by a supervisor
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        null=True,
    )

    WORKSTATION = 1
    LAPTOP = 2
    SERVER = 3
    NETWORK = 4
    PRINTER = 5
    SCANNER = 6
    OTHER_PERIPHERAL = 7
    SOFTWARE = 8
    ACCESS = 9

    CATEGORY_CHOICES = (
        (WORKSTATION, 'Workstation'),
        (LAPTOP, 'Laptop'),
        (SERVER, 'Server'),
        (NETWORK, 'Network'),
        (PRINTER, 'Printer'),
        (SCANNER, 'Scanner'),
        (OTHER_PERIPHERAL, 'Other Peripheral'),
        (SOFTWARE, 'Software'),
        (ACCESS, 'Access'),
    )

    # To be assigned by a supervisor
    category = models.IntegerField(
        choices=CATEGORY_CHOICES,
        null=True
    )

    assignment_date = models.DateTimeField(
        blank=True,
        null=True,
    )

    # To be filled by IT or a supervisor
    resolution = models.TextField(
        default=''
    )

    OPEN = 1
    CLOSED = 2

    STATUS_CHOICES = (
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    )

    # To be changed by IT or a supervisor
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=OPEN,
    )

    closed_date = models.DateTimeField(
        blank=True,
        null=True,
    )


class Note(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        related_name='notes',
        on_delete=models.PROTECT,
    )

    user = models.ForeignKey(
        HelpDeskUser,
        related_name='notes',
        on_delete=models.PROTECT,
    )

    # Automatically created
    created_date = models.DateTimeField(
        auto_now_add=True
    )

    text = models.TextField(
        default=''
    )
