from csv import DictReader
import logging

from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User

logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='w',
    format='%(asctime)s, %(levelname)s, %(message)s'
)

TABLES = {
    User: "users.csv",
    Category: "category.csv",
    Genre: "genre.csv",
    Title: "titles.csv",
    Review: "review.csv",
    Comment: "comments.csv",
    Title.genre.through: "genre_title.csv",
}


class Command(BaseCommand):
    help = "Import from csv to db"

    def handle(self, *args, **kwargs):
        for model, csv, in TABLES.items():
            with open(f"./static/data/{csv}", encoding="utf-8") as file:
                if model.objects.exists():
                    logging.error('Data already loaded... Exiting.')
                    continue
                reader = DictReader(file)
                model.objects.bulk_create(model(**data) for data in reader)
            self.stdout.write(self.style.SUCCESS("Data is loaded"))
