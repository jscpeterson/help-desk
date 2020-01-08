from django.contrib.auth.models import AbstractUser
from django.db import models

# User Groups
GROUP_SUPPORT = 'Support'
GROUP_SUPERVISOR = 'Supervisor'


class HelpDeskUser(AbstractUser):

    def __str__(self):
        return self.first_name + ' ' + self.last_name
