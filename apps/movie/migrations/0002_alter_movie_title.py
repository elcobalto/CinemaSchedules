# Generated by Django 4.0.4 on 2022-04-14 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movie", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="title",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
