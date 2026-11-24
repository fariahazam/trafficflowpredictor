from django.core.management.base import BaseCommand
from dashboard.services.data_loader import TrafficDataLoader
from dashboard.services.model import TrafficPredictor


class Command(BaseCommand):
    help = 'Train the traffic prediction model and save it to disk.'

    def handle(self, *args, **options):
        TrafficPredictor().train(TrafficDataLoader.get_data())
        self.stdout.write(self.style.SUCCESS('Model trained and saved.'))