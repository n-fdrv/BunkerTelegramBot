from random import randint

from django.conf import settings

from bot.models import Cart, Character, Game, Room, User


async def get_random_cart(cart_type: str) -> Cart:
    """Метод получения случайной карты."""
    return await Cart.objects.filter(type=cart_type).order_by("?").afirst()


async def generate_game(room: Room):
    """Метод генерации случайной игры."""
    epidemia = await get_random_cart("epidemia_type")
    epidemia_time = randint(1, 10)
    bunker = await get_random_cart("bunker_type_cart")
    room_one = await get_random_cart("room_cart")
    room_two = await get_random_cart("room_cart")
    room_three = await get_random_cart("room_cart")

    bunker_place_amount = (
        await User.objects.filter(room=room).acount()
        // settings.BUNKER_PLACE_DIVIDER
    )

    return await Game.objects.acreate(
        epidemia=epidemia,
        bunker_place_amount=bunker_place_amount,
        epidemia_time=epidemia_time,
        bunker_type=bunker,
        room_one=room_one,
        room_two=room_two,
        room_three=room_three,
    )


async def generate_character(user: User, game: Game):
    """Метод генерации случайного персонажа."""
    good_health = randint(1, 100) <= settings.HEALTH_CHANCE
    no_phobia = randint(1, 100) <= settings.PHOBIA_CHANCE
    getero_orientation = randint(1, 100) < settings.ORIENTATION_CHANCE
    age = randint(settings.MIN_AGE_VALUE, settings.MAX_AGE_VALUE)

    gender = await get_random_cart("gender_cart")
    orientation = await get_random_cart("orientation_cart")
    profession = await get_random_cart("prof_cart")
    health = await get_random_cart("health_cart")
    phobia = await get_random_cart("phobia_cart")
    personality = await get_random_cart("personality_cart")
    hobby = await get_random_cart("hobby_cart")
    information = await get_random_cart("ad_info_cart")
    item = await get_random_cart("item_cart")
    action_one = await get_random_cart("action_cart")
    action_two = await get_random_cart("action_cart")

    if good_health:
        health = await Cart.objects.aget(name="Полностью здоров.")
    if no_phobia:
        phobia = await Cart.objects.aget(name="Отсутствует")
    if getero_orientation:
        orientation = await Cart.objects.aget(name="Гетеросексуал")

    return await Character.objects.acreate(
        user=user,
        age=age,
        gender=gender,
        orientation=orientation,
        profession=profession,
        health=health,
        phobia=phobia,
        personality=personality,
        hobby=hobby,
        information=information,
        item=item,
        action_one=action_one,
        action_two=action_two,
        game=game,
    )
