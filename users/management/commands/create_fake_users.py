from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from users.models import HelpDeskUser, GROUP_SUPPORT, GROUP_SUPERVISOR
from faker import Faker

faker = Faker()
SUGGESTED_PASSWORD = 'HelpDesk1'
GROUPS = [GROUP_SUPPORT, GROUP_SUPERVISOR]


class Command(BaseCommand):
    help = 'Creates a regular user, a support user, and a supervisor user'

    def handle(self, *args, **kwargs):
        """ Handles creating users"""

        first_name = faker.first_name()
        last_name = faker.last_name()

        user = HelpDeskUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=first_name[0] + last_name,
        )
        user.set_password(SUGGESTED_PASSWORD)
        user.save(update_fields=['password'])
        print('Regular user {} created'.format(user.username))

        for group_name in GROUPS:
            first_name = faker.first_name()
            last_name = faker.last_name()

            user = HelpDeskUser.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=first_name[0] + last_name,
            )
            user.set_password(SUGGESTED_PASSWORD)
            user.save(update_fields=['password'])
            try:
                group = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                group = Group.objects.create(name=group_name)
            user.groups.add(group)
            print('{group} user {username} created'.format(group=group_name, username=user.username))
