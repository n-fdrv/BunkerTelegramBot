from random import randint

from bot.constants import messages
from bot.models import Room, User
from bot.utils.character_generator import generate_character


async def create_room(user: User):
    """Метод создания комнаты."""
    if user.room:
        return user.room, False
    number = randint(100000, 999999)
    while await Room.objects.filter(slug=number).acount() > 0:
        number = randint(100000, 999999)
    room = await Room.objects.acreate(slug=number, admin=user)
    user.room = room
    await user.asave(update_fields=("room",))
    return room, True


async def get_room(room_slug):
    """Метод проверки существования и получения комнаты."""
    if not room_slug.isdigit():
        return None
    room_slug = int(room_slug)
    is_exist = await Room.objects.filter(slug=room_slug).aexists()
    if is_exist:
        return await Room.objects.select_related("admin").aget(slug=room_slug)
    return None


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
    async for player in User.objects.filter(room=room).all():
        await generate_character(player)
    return messages.GAME_STARTED_MESSAGE, True
