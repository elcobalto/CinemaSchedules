# Generated by Django 4.0.4 on 2022-06-18 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cinema", "0013_showing_town_delete_schedule_cinema_town"),
    ]

    operations = [
        migrations.AddField(
            model_name="showing",
            name="format",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
