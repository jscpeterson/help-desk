from django.contrib import admin

from tickets.models import Ticket
from users.models import HelpDeskUser

admin.site.register(HelpDeskUser)
admin.site.register(Ticket)
