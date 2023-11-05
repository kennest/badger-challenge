import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError, IntegrityError
from badger.models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write("waiting for db...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
                try:
                    user = User.objects.create_superuser(username="admin", password="jjks", email="admin@gmail.com")
                    Badge.objects.create(name='Star', description='Your model has more than 1k views',
                                         image='star.png')
                    Badge.objects.create(name='Collector',
                                         description='You have uploaded more than 5 models',
                                         image='collector.png')
                    Badge.objects.create(name='Pioneer',
                                         description='You have reached 1 year on the site, you receive a badge Pionneer',
                                         image='pionneer.png')
                    self.stdout.write(f"Super user created : [ {user} ]", style_func=self.style.SUCCESS)
                    self.stdout.write(f"continue...", style_func=self.style.SUCCESS)
                except IntegrityError:
                    self.stdout.write("Super user already exists, continue...", style_func=self.style.SUCCESS)
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 second ...", style_func=self.style.WARNING)
                time.sleep(1)
