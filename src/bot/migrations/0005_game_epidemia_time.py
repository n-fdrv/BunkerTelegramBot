# Generated by Django 4.2.6 on 2023-12-26 14:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0004_remove_game_bunker_game_bunker_type_game_room_one_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="epidemia_time",
            field=models.IntegerField(
                default=1, verbose_name="Лет до выхода на поверхность"
            ),
            preserve_default=False,
        ),
    ]
