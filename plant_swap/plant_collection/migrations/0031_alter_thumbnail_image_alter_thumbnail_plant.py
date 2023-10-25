# Generated by Django 4.2.3 on 2023-10-25 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("plant_collection", "0030_thumbnail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="thumbnail",
            name="image",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="thumbnail",
                to="plant_collection.image",
            ),
        ),
        migrations.AlterField(
            model_name="thumbnail",
            name="plant",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="thumbnail",
                to="plant_collection.plant",
            ),
        ),
    ]