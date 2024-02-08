from datetime import datetime
from random import randint

from django.conf import settings

from game.models import Game, Room, TypeInformationCarts
from game.utils.cart import get_random_unique_information_cart
from game.utils.character import create_character

from bot.constants import messages
from bot.models import User
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
    game = await create_game(room)
    async for player in (
        User.objects.select_related("room").filter(room=room).all()
    ):
        player.game = game
        await game.users.aadd(player)
        await player.asave(update_fields=("game",))
        await create_character(player, game)
    return messages.GAME_STARTED_MESSAGE, True


async def create_game(room: Room) -> Game:
    """Метод создания игры."""
    epidemia_time = randint(1, 10)
    bunker_place_amount = (
        await User.objects.filter(room=room).acount()
        // settings.BUNKER_PLACE_DIVIDER
    )
    game = await Game.objects.acreate(
        epidemia_time=epidemia_time,
        bunker_place_amount=bunker_place_amount,
    )
    epidemia = await get_random_unique_information_cart(
        TypeInformationCarts.EPIDEMIA, game
    )
    bunker_type = await get_random_unique_information_cart(
        TypeInformationCarts.BUNKER_TYPE, game
    )
    room_one = await get_random_unique_information_cart(
        TypeInformationCarts.BUNKER_ROOM, game
    )
    room_two = await get_random_unique_information_cart(
        TypeInformationCarts.BUNKER_ROOM, game
    )
    room_three = await get_random_unique_information_cart(
        TypeInformationCarts.BUNKER_ROOM, game
    )
    await game.information_carts.aadd(
        epidemia, bunker_type, room_one, room_two, room_three
    )
    return game


async def close_game(game: Game) -> Game:
    """Закрывает игру и удаляет пользователям поле в игре."""
    await game.users.aupdate(game=None)
    game.closed_date = datetime.now()
    game.closed = True
    await game.asave(update_fields=("closed_date", "closed"))
    return game


async def get_bunker_info_text(game: Game):
    """Метод получения информации о бункере."""
    room_text = ""
    room_number = 1
    async for room in game.unique_carts.filter(
        type=TypeInformationCarts.BUNKER_ROOM
    ):
        room_text += f"<b>{room_number}. {room}</b>\n"
        room_number += 1
    return messages.BUNKER_GET_MESSAGE.format(
        await game.unique_carts.filter(
            type=TypeInformationCarts.BUNKER_TYPE
        ).alast(),
        game.bunker_place_amount,
        room_text,
    )


async def get_players_in_game_message(game: Game):
    """Метод формирования сообщения об игроках в игре."""
    players_amount = await User.objects.filter(game=game).acount()
    players_info = ""
    async for player in User.objects.filter(game=game).all():
        players_info += f"- {get_user_url(player)}\n"
    return messages.GAME_SETTINGS_MESSAGE.format(
        game.pk, players_amount, players_info
    )
