# Generated by Django 4.0.4 on 2022-04-13 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cinema", "0005_remove_cinema_city"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cinema",
            old_name="title",
            new_name="name",
        ),
    ]
