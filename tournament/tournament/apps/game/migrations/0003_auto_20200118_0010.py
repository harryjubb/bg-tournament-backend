# Generated by Django 3.0.2 on 2020-01-18 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0002_auto_20200117_2343"),
    ]

    operations = [
        migrations.RenameField(
            model_name="game", old_name="length", new_name="max_length",
        ),
        migrations.AddField(
            model_name="game",
            name="min_length",
            field=models.DurationField(default=0),
            preserve_default=False,
        ),
    ]
