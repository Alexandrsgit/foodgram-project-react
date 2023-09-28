import csv
import os
from foodgram_backend import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Tag


def ingredient_create(row):
    if len(row) >= 2:
        return Ingredient(
            name=row[0],
            measurement_units=row[1]
        )
    else:
        return None


def tag_create(row):
    if len(row) >= 3:
        return Tag(
            name=row[0],
            color=row[1],
            slug=row[2]
        )
    else:
        return None


class Command(BaseCommand):
    help = 'Импорт данных из CSV'

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, 'ingredients.csv')
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            ingredients = [ingredient_create(row) for row in reader]
            Ingredient.objects.bulk_create(ingredients)
        self.stdout.write(' - Данные успешно импортированны!')

        path = os.path.join(settings.BASE_DIR, 'tags.csv')
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            tags = [tag_create(row) for row in reader]
            Tag.objects.bulk_create(tags)
        self.stdout.write(' - Данные успешно импортированны!')
