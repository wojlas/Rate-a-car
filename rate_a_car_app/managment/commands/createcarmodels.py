from django.core.management import BaseCommand

from rate_a_car_app.managment.commands._private import create_fake_models


class Command(BaseCommand):
    help = 'Fake car models'

    def handle(self, *args, **options):
        create_fake_models()
        self.stdout.write(self.style.SUCCESS("Succesfully create car models"))