from django.contrib.auth.models import AbstractUser
from django.db import models

# User Groups
GROUP_SUPPORT = 'Support'
GROUP_SUPERVISOR = 'Supervisor'
GROUP_DIVISION_HEAD = 'Division Head'


class HelpDeskUser(AbstractUser):

    def is_supervisor(self):
        return self.groups.filter(name=GROUP_SUPERVISOR).exists()

    def is_support(self):
        return self.groups.filter(name=GROUP_SUPPORT).exists()

    def __str__(self):
        return self.first_name + ' ' + self.last_name
