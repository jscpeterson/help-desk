# Generated by Django 3.0.2 on 2020-01-07 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_ticket_closed_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='assignment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]