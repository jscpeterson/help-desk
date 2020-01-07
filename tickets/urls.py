from django.urls import path
from . import views

app_name = 'tickets'
urlpatterns = [

    path('', views.home, name='home'),

    # User Tickets
    path('user/', views.view_user_tickets, name='view_user_tickets'),
    # User New Ticket Submission
    path('new/', views.new_ticket, name='new_ticket'),
    # ? User Ticket Submitted Confirmation ?

    # Supervisor Unassigned Tickets
    path('unassigned/', views.view_unassigned_tickets, name='view_unassigned_tickets'),
    # Supervisor Ticket Assignment
    path('<int:ticket_id>/assign/', views.assign_ticket, name='assign_ticket'),

    # Support Assigned Tickets
    path('assigned/', views.view_assigned_tickets, name='view_assigned_tickets'),
    # Support Ticket Resolution
    path('<int:ticket_id>/resolve/', views.resolve_ticket, name='resolve_ticket'),
    # ? Support Ticket Resolution Confirmation ?

    # ? Supervisor Assigned/In Progress Tickets ?
    # ? All Tickets ?

    # Ticket View
    # User View

]
