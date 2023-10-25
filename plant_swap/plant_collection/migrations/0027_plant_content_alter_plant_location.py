# Generated by Django 4.2.3 on 2023-10-25 09:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plant_collection", "0026_alter_plant_location"),
    ]

    operations = [
        migrations.AddField(
            model_name="plant",
            name="content",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="plant",
            name="location",
            field=models.CharField(
                blank=True,
                default=None,
                help_text="City, State",
                max_length=24,
                null=True,
            ),
        ),
    ]
