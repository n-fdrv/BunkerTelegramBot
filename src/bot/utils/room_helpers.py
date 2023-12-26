from random import randint

from bot.models import Room, User


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


async def get_room(room_slug: int):
    """Метод проверки существования и получения комнаты."""
    is_exist = await Room.objects.filter(slug=room_slug).aexists()
    if is_exist:
        return await Room.objects.select_related("admin").aget(slug=room_slug)
    return None
