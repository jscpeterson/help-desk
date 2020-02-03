from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from users.models import HelpDeskUser, GROUP_SUPPORT, GROUP_SUPERVISOR

GROUPS = [GROUP_SUPPORT, GROUP_SUPERVISOR]


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        pass
