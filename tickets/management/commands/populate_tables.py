import io
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from tickets.models import JobTitle, Division, Building


class Command(BaseCommand):
    help = "Populates buildings, job titles, and division tables from txt files"

    def handle(self, *args, **kwargs):
        resources_dir = os.path.join(settings.BASE_DIR, 'resources')
        resources = {
            ('buildings.txt', Building),
            ('divisions.txt', Division),
            ('jobtitles.txt', JobTitle),
        }

        for resource_location, resource_model in resources:
            f = io.open(os.path.join(resources_dir, resource_location))
            skips = 0
            created = 0
            for item in f.read().split('\n'):
                if resource_model.objects.filter(name=item).exists():
                    skips += 1
                else:
                    created += 1
                    resource_model.objects.create(name=item)
            print('Created {created} objects and skipped {skips} lines from {location}.'.format(
                created=created,
                skips=skips,
                location=resource_location,
            ))
            f.close()
