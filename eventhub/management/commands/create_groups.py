from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Group.objects.filter(name="Commercial"):
            Group.objects.create(name="Commercial")
            self.stdout.write(self.style.SUCCESS("Commercial group created"))

        if not Group.objects.filter(name="Support"):
            Group.objects.create(name="Support")
            self.stdout.write(self.style.SUCCESS("Support group created"))