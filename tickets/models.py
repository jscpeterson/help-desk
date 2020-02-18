import io
import os

from django.db import models

from helpdesk.settings.base import BASE_DIR
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

    MOVE_REQUEST = 10
    NEW_USER = 11

    CATEGORY_CHOICES = (
        (WORKSTATION, 'Workstation'),
        (LAPTOP, 'Laptop'),
        (SERVER, 'Server'),
        (NETWORK, 'Network'),
        (PRINTER, 'Printer'),
        (SCANNER, 'Scanner'),
        (OTHER_PERIPHERAL, 'Other Peripheral'),
        (SOFTWARE, 'Software'),
    )

    DIVISION_HEAD_CATEGORY_CHOICES = (
        (MOVE_REQUEST, 'Move Request'),
        (NEW_USER, 'New User'),
    )

    # To be assigned by a supervisor
    category = models.IntegerField(
        choices=CATEGORY_CHOICES + DIVISION_HEAD_CATEGORY_CHOICES,
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


RESOURCES_DIR = os.path.join(BASE_DIR, 'resources')


def get_choice_list_from_resources(filename):
    f = io.open(os.path.join(RESOURCES_DIR, filename))
    choice_list = [[i+1, building] for i, building in enumerate(f.read().split('\n'))]
    f.close()
    return choice_list


class MoveRequestTicket(Ticket):
    BUILDING_CHOICES = get_choice_list_from_resources('buildings.txt')

    old_building = models.IntegerField(
        choices=BUILDING_CHOICES,
    )

    new_building = models.IntegerField(
        choices=BUILDING_CHOICES,
    )

    DIVISION_CHOICES = get_choice_list_from_resources('divisions.txt')

    old_division = models.IntegerField(
        choices=DIVISION_CHOICES,
    )

    new_division = models.IntegerField(
        choices=DIVISION_CHOICES,
    )

    old_room_number = models.CharField(
        max_length=10,
    )

    new_room_number = models.CharField(
        max_length=10,
    )

    scheduled_move_date = models.DateTimeField(
    )


class NewUserTicket(Ticket):

    name = models.CharField(
        max_length=120,
    )

    BUILDING_CHOICES = get_choice_list_from_resources('buildings.txt')

    building = models.IntegerField(
        choices=BUILDING_CHOICES,
    )

    DIVISION_CHOICES = get_choice_list_from_resources('divisions.txt')

    division = models.IntegerField(
        choices=DIVISION_CHOICES,
    )

    CMS_ACCESS_CHOICES = get_choice_list_from_resources('cmsaccess.txt')

    cms_access = models.IntegerField(
        choices=CMS_ACCESS_CHOICES,
    )

    JOB_TITLE_CHOICES = get_choice_list_from_resources('jobtitles.txt')

    job_title = models.IntegerField(
        choices=JOB_TITLE_CHOICES,
    )

    room_number = models.CharField(
        max_length=10,
    )

    needs_computer = models.BooleanField(
        default=False,
    )

    needs_email_account = models.BooleanField(
        default=False,
    )

    # Date new user will begin work
    start_date = models.DateTimeField(
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
