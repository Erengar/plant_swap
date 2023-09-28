# Generated by Django 4.2.3 on 2023-09-27 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("plant_collection", "0013_alter_plant_picture"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="plant",
            name="picture",
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="pics")),
                (
                    "plant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="picture",
                        to="plant_collection.plant",
                    ),
                ),
            ],
        ),
    ]