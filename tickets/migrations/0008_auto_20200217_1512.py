# Generated by Django 3.0.2 on 2020-02-17 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0007_auto_20200207_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoveRequestTicket',
            fields=[
                ('ticket_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tickets.Ticket')),
                ('building', models.IntegerField(blank=True, choices=[[1, 'Steve Schiff Building'], [2, 'Juvenile Justice Center'], [3, 'Grand Jury at District Court']], null=True)),
                ('division', models.IntegerField(blank=True, choices=[[1, 'Administration Team'], [2, 'Admin Fiscal Team'], [3, 'Admin HR Team'], [4, 'Admin IT Team'], [5, 'Admin VIP Team'], [6, 'General Crimes Blue Team'], [7, 'General Crimes Red Team'], [8, 'General Crimes Green Team'], [9, 'General Crimes PPP Team'], [10, 'Major Crimes Blue Team'], [11, 'Major Crimes Red Team'], [12, 'Major Crimes Green Team'], [13, 'Major Crimes SVU Team'], [14, 'Grand Jury Team'], [15, 'Intake Team'], [16, 'Juvenile Team'], [17, 'Metro Team'], [18, 'Process Locate Team'], [19, 'Scan Project Team'], [20, 'Special Proceedings Team']], null=True)),
                ('scheduled_move_date', models.DateTimeField(blank=True, null=True)),
            ],
            bases=('tickets.ticket',),
        ),
        migrations.CreateModel(
            name='NewUserTicket',
            fields=[
                ('ticket_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tickets.Ticket')),
                ('building', models.IntegerField(blank=True, choices=[[1, 'Steve Schiff Building'], [2, 'Juvenile Justice Center'], [3, 'Grand Jury at District Court']], null=True)),
                ('division', models.IntegerField(blank=True, choices=[[1, 'Administration Team'], [2, 'Admin Fiscal Team'], [3, 'Admin HR Team'], [4, 'Admin IT Team'], [5, 'Admin VIP Team'], [6, 'General Crimes Blue Team'], [7, 'General Crimes Red Team'], [8, 'General Crimes Green Team'], [9, 'General Crimes PPP Team'], [10, 'Major Crimes Blue Team'], [11, 'Major Crimes Red Team'], [12, 'Major Crimes Green Team'], [13, 'Major Crimes SVU Team'], [14, 'Grand Jury Team'], [15, 'Intake Team'], [16, 'Juvenile Team'], [17, 'Metro Team'], [18, 'Process Locate Team'], [19, 'Scan Project Team'], [20, 'Special Proceedings Team']], null=True)),
                ('cms_access', models.IntegerField(blank=True, choices=[[1, 'None Needed'], [2, 'Guest (Read Only)'], [3, 'DAStaff (Read and Write)']], null=True)),
                ('job_title', models.IntegerField(blank=True, choices=[[1, 'Administrative Secretary'], [2, 'Assistant Trial Attorney'], [3, 'Associate Trial Attorney'], [4, 'Chief Deputy District Attorney'], [5, 'Chief Financial Officer'], [6, 'Clerk'], [7, 'Clerk Apprentice'], [8, 'Clerk Specialist'], [9, 'DataBase Administrator'], [10, 'Deputy District Attorney'], [11, 'District Office Manager'], [12, 'Extern-Intern-Temp'], [13, 'Financial Assistant'], [14, 'Financial Specialist'], [15, 'Financial Specialist Supervisor'], [16, 'Human Resources Administrator'], [17, 'Human Resources Coordinator'], [18, 'Information Systems Administrator'], [19, 'Information Systems Assistant'], [20, 'Information Systems Manager'], [21, 'Investigator'], [22, 'Law Student'], [23, 'Lead Investigator'], [24, 'Program Administrator'], [25, 'Program Assistant'], [26, 'Program Specialist'], [27, 'Prosecution Assistant'], [28, 'Prosecution Specialist'], [29, 'Secretary'], [30, 'Senior Investigator'], [31, 'Senior Secretary'], [32, 'Senior Trial Attorney'], [33, 'Senior Victim Advocate'], [34, 'Special Program Director'], [35, 'Supervising Secretary'], [36, 'Victim Advocate'], [37, 'Victim Advocate Administrator'], [38, 'Victim Advocate Coordinator']], null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
            ],
            bases=('tickets.ticket',),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='category',
            field=models.IntegerField(choices=[(1, 'Workstation'), (2, 'Laptop'), (3, 'Server'), (4, 'Network'), (5, 'Printer'), (6, 'Scanner'), (7, 'Other Peripheral'), (8, 'Software')], null=True),
        ),
    ]
