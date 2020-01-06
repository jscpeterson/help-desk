from django.contrib.auth.models import AbstractUser
from django.db import models

# User Groups
GROUP_SUPPORT = 'Support'
GROUP_SUPERVISOR = 'Supervisor'


class HelpDeskUser(AbstractUser):
    pass
