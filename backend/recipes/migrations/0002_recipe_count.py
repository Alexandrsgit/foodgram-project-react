# Generated by Django 3.2.3 on 2023-08-20 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='count',
            field=models.IntegerField(default=0, verbose_name='Колличество добавлений рецепта'),
        ),
    ]
