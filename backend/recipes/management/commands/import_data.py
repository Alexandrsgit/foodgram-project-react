import csv
import os
import logging
from foodgram_backend import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Tag


logger = logging.getLogger(__name__)


def ingredient_create(row):
    if len(row) == 2:
        return Ingredient(
            name=row[0],
            measurement_units=row[1]
        )
    else:
        raise ValueError(f'В файле должны быть 2 колонки с данными,'
                         f'но их {len(row)}')


def tag_create(row):
    if len(row) == 3:
        return Tag(
            name=row[0],
            color=row[1],
            slug=row[2]
        )
    else:
        raise ValueError(f'В файле должны быть 3 колонки с данными,'
                         f'но их {len(row)}')


class Command(BaseCommand):
    help = 'Импорт данных из CSV'

    def handle(self, *args, **options):
        if Ingredient.objects.exists():
            logger.info(' Ингредиенты уже испортированы в базу данных.')
        else:
            ingredients_file_path = os.path.join(settings.BASE_DIR, 'data',
                                                 'ingredients.csv')
            with open(ingredients_file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                ingredients = [ingredient_create(row) for row in reader]
                Ingredient.objects.bulk_create(ingredients)
            logger.info(' Данные успешно импортированы из ingredients.csv')

        if Tag.objects.exists():
            logger.info(' Теги уже импортированы в базу данных.')
        else:
            tags_file_path = os.path.join(settings.BASE_DIR, 'data',
                                          'tags.csv')
            with open(tags_file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                tags = [tag_create(row) for row in reader]
                Tag.objects.bulk_create(tags)
            logger.info(' Данные успешно импортированы из tags.csv')
