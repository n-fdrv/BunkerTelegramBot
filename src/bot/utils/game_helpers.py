from bot.constants import messages
from bot.models import Game, Room, User
from bot.utils.game_generator import generate_character, generate_game
from bot.utils.user_helpers import get_user_url


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
    async for player in (
        User.objects.select_related("room").filter(room=room).all()
    ):
        player.game = game
        await player.asave(update_fields=("game",))
        await generate_character(player, game)
    return messages.GAME_STARTED_MESSAGE, True


async def get_players_in_game_message(game: Game):
    """Метод формирования сообщения об игроках в игре."""
    players_amount = await User.objects.filter(game=game).acount()
    players_info = ""
    async for player in User.objects.filter(game=game).all():
        players_info += f"- {get_user_url(player)}\n"
    return messages.GAME_SETTINGS_MESSAGE.format(
        game.pk, players_amount, players_info
    )
