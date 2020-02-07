from django.urls import path
from . import views

app_name = 'tickets'
urlpatterns = [

    path('', views.home, name='home'),

    # User Tickets
    path('user/', views.view_user_tickets, name='view_user_tickets'),
    # User New Ticket Submission
    path('new/', views.new_ticket, name='new_ticket'),

    # Supervisor Unassigned Tickets
    path('unassigned/', views.view_unassigned_tickets, name='view_unassigned_tickets'),
    # Supervisor Ticket Assignment
    path('assign/<int:ticket_id>/', views.assign_ticket, name='assign_ticket'),

    # Support Assigned Tickets
    path('assigned/', views.view_assigned_tickets, name='view_assigned_tickets'),
    # Support Ticket Resolution
    path('resolve/<int:ticket_id>/', views.resolve_ticket, name='resolve_ticket'),

    # Support / Supervisor Closed Tickets
    path('closed/', views.closed_tickets, name='view_closed_tickets'),

    # Search Tickets
    path('search/', views.search_tickets, name="search_tickets"),

    # Ticket Detail View
    path('<int:ticket_id>', views.view_ticket, name='view_ticket'),

    # Add Note
    path('add_note/<int:ticket_id>', views.add_note, name='add_note'),

]
