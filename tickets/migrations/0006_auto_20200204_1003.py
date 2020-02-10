# Generated by Django 3.0.2 on 2020-02-04 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0005_auto_20200204_0924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='notes',
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(default='')),
                ('ticket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='notes', to='tickets.Ticket')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='notes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
