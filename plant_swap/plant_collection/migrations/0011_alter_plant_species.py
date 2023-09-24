# Generated by Django 4.2.3 on 2023-09-24 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("plant_collection", "0010_alter_plant_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plant",
            name="species",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="plants",
                to="plant_collection.species",
            ),
        ),
    ]
