from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from users.models import GROUP_SUPPORT, GROUP_SUPERVISOR

GROUPS = [GROUP_SUPPORT, GROUP_SUPERVISOR]


class Command(BaseCommand):
    help = 'Creates groups for application'

    def handle(self, *args, **kwargs):
        """ Handles creating groups """

        for group_name in GROUPS:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                print('Group {group} created'.format(group=group_name))
            else:
                print('Group {group} already exists'.format(group=group_name))
