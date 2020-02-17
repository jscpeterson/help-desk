# Generated by Django 3.0.2 on 2020-02-17 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0008_auto_20200217_1512'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moverequestticket',
            old_name='building',
            new_name='new_building',
        ),
        migrations.RenameField(
            model_name='moverequestticket',
            old_name='division',
            new_name='new_division',
        ),
        migrations.AddField(
            model_name='moverequestticket',
            name='old_building',
            field=models.IntegerField(blank=True, choices=[[1, 'Steve Schiff Building'], [2, 'Juvenile Justice Center'], [3, 'Grand Jury at District Court']], null=True),
        ),
        migrations.AddField(
            model_name='moverequestticket',
            name='old_division',
            field=models.IntegerField(blank=True, choices=[[1, 'Administration Team'], [2, 'Admin Fiscal Team'], [3, 'Admin HR Team'], [4, 'Admin IT Team'], [5, 'Admin VIP Team'], [6, 'General Crimes Blue Team'], [7, 'General Crimes Red Team'], [8, 'General Crimes Green Team'], [9, 'General Crimes PPP Team'], [10, 'Major Crimes Blue Team'], [11, 'Major Crimes Red Team'], [12, 'Major Crimes Green Team'], [13, 'Major Crimes SVU Team'], [14, 'Grand Jury Team'], [15, 'Intake Team'], [16, 'Juvenile Team'], [17, 'Metro Team'], [18, 'Process Locate Team'], [19, 'Scan Project Team'], [20, 'Special Proceedings Team']], null=True),
        ),
    ]
