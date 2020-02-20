from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from users.models import HelpDeskUser, GROUP_SUPPORT, GROUP_SUPERVISOR, GROUP_DIVISION_HEAD

GROUPS = [GROUP_SUPPORT, GROUP_SUPERVISOR, GROUP_DIVISION_HEAD]


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--group', type=str, required=True)
        parser.add_argument('--username', type=str, required=True)

    def handle(self, *args, **kwargs):
        group_name = " ".join([word.capitalize() for word in kwargs['group'].split(" ")])
        if group_name not in GROUPS:
            print('Group not recognized. Groups are as follows: {}'.format(', '.join(GROUPS)))
            return

        if not HelpDeskUser.objects.filter(username=kwargs['username']).exists():
            print('User {} not found. Please enter a username.'.format(kwargs['username']))
            return

        user = HelpDeskUser.objects.get(username=kwargs['username'])
        group = Group.objects.get(name=group_name)

        if user.groups.filter(name=group).exists():
            print('{user} already has {group} privileges.'.format(
                group=group,
                user=user,
            ))
            return

        user.groups.add(group)
        print('{user} now has {group} privileges.'.format(
            group=group,
            user=user,
        ))
