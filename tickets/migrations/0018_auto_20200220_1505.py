# Generated by Django 3.0.2 on 2020-02-20 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0017_auto_20200219_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='category',
            field=models.IntegerField(choices=[(1, 'Workstation'), (2, 'Laptop'), (3, 'Server'), (4, 'Network'), (5, 'Printer'), (6, 'Scanner'), (7, 'Other Peripheral'), (8, 'Software'), (9, 'Access'), (10, 'Move Request'), (11, 'New User')], null=True),
        ),
    ]
