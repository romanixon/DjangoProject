# Generated by Django 4.2 on 2023-04-26 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0002_category_subsribers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='subsribers',
            new_name='subscribers',
        ),
    ]
