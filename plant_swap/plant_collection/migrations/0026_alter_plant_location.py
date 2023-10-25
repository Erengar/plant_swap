# Generated by Django 4.2.3 on 2023-10-24 22:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plant_collection", "0025_alter_plant_location"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plant",
            name="location",
            field=models.CharField(
                blank=True,
                default=None,
                help_text="City, State",
                max_length=64,
                null=True,
            ),
        ),
    ]
