# Generated by Django 4.0.4 on 2022-04-14 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cinema", "0010_schedule"),
    ]

    operations = [
        migrations.AddField(
            model_name="cinema",
            name="keyword",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
