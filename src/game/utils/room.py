from random import randint

from game.models import Room

from bot.constants.messages import ROOM_GET_MESSAGE
from bot.models import User
from bot.utils.user_helpers import get_user_url


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


async def get_players_in_room_message(room: Room):
    """Метод формирования сообщения об игроках в комнате."""
    players_amount = await User.objects.filter(room=room).acount()
    players_info = ""
    async for player in User.objects.filter(room=room).all():
        players_info += f"\n- {get_user_url(player)}"
        if player == room.admin:
            players_info += " (Администратор)"
    return ROOM_GET_MESSAGE.format(room.slug, players_amount, players_info)
