# Generated by Django 3.2.3 on 2023-09-12 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_subscribed',
        ),
    ]