# Generated by Django 4.2.9 on 2024-02-07 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("bot", "0001_initial"),
        ("game", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="game",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="game.game",
                verbose_name="Игра",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="room",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="game.room",
                verbose_name="Комната",
            ),
        ),
    ]
