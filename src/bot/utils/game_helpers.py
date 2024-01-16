from bot.constants import messages
from bot.models import Room, User
from bot.utils.game_generator import generate_character, generate_game


async def start_game(room: Room):
    """Метод старта игры."""
    players_count = await User.objects.filter(room=room).acount()
    players_min_value = 1
    if players_count < players_min_value:
        return (
            messages.NOT_ENOUGH_PLAYERS_MESSAGE.format(players_min_value),
            False,
        )
    room.started = True
    await room.asave(update_fields=("started",))
    game = await generate_game(room)
    async for player in User.objects.select_related("room").filter(
        room=room
    ).all():
        player.game = game
        await player.asave(update_fields=("game",))
        await generate_character(player, game)
    return messages.GAME_STARTED_MESSAGE, True
