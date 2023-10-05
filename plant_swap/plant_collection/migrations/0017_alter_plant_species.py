# Generated by Django 4.2.3 on 2023-10-04 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("plant_collection", "0016_plant_likes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plant",
            name="species",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="plants",
                to="plant_collection.species",
            ),
        ),
    ]