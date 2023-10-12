# Generated by Django 4.2.3 on 2023-10-09 23:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plant_collection", "0020_alter_trade_initiator_alter_trade_recipient"),
    ]

    operations = [
        migrations.AddField(
            model_name="trade",
            name="offered_finalized",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="trade",
            name="requested_finalized",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="trade",
            name="accepted",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]