# Generated by Django 4.1.5 on 2023-02-26 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_rename_favourite_favorite'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='title',
            new_name='product',
        ),
    ]
