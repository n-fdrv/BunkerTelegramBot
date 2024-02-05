from random import randint

from django.conf import settings

from bot.models import Cart, Character, Game, Room, User


async def get_random_cart(cart_type: str, exclude_list=None) -> Cart:
    """Метод получения случайной карты."""
    if exclude_list is None:
        exclude_list = []
    return (
        await Cart.objects.filter(type=cart_type)
        .order_by("?")
        .exclude(pk__in=exclude_list)
        .afirst()
    )


async def generate_game(room: Room) -> Game:
    """Метод генерации случайной игры."""
    epidemia = await get_random_cart("epidemia_type")
    epidemia_time = randint(1, 10)
    bunker = await get_random_cart("bunker_type_cart")
    room_one = await get_random_cart("room_cart")
    room_two = await get_random_cart("room_cart", [room_one.pk])
    room_three = await get_random_cart("room_cart", [room_one.pk, room_two.pk])

    bunker_place_amount = (
        await User.objects.filter(room=room).acount()
        // settings.BUNKER_PLACE_DIVIDER
    )

    game = await Game.objects.acreate(
        epidemia=epidemia,
        bunker_place_amount=bunker_place_amount,
        epidemia_time=epidemia_time,
        bunker_type=bunker,
        room_one=room_one,
        room_two=room_two,
        room_three=room_three,
    )
    game.epidemia = epidemia
    return game


async def generate_character(
    user: User, game: Game, used_carts=None
) -> tuple[Character, list[int]]:
    """Метод генерации случайного персонажа."""
    if used_carts is None:
        used_carts = []
    good_health = randint(1, 100) <= settings.HEALTH_CHANCE
    no_phobia = randint(1, 100) <= settings.PHOBIA_CHANCE
    getero_orientation = randint(1, 100) <= settings.ORIENTATION_CHANCE
    young_age = randint(1, 100) <= settings.YOUNG_AGE_CHANCE

    age = randint(settings.AVERAGE_AGE_VALUE, settings.MAX_AGE_VALUE)

    if young_age:
        age = randint(settings.MIN_AGE_VALUE, settings.AVERAGE_AGE_VALUE)

    gender = await get_random_cart("gender_cart")
    profession = await get_random_cart("prof_cart", used_carts)
    personality = await get_random_cart("personality_cart", used_carts)
    hobby = await get_random_cart("hobby_cart", used_carts)
    information = await get_random_cart("ad_info_cart", used_carts)
    item = await get_random_cart("item_cart", used_carts)
    action_one = await get_random_cart("action_cart", used_carts)
    used_carts.append(action_one.pk)
    action_two = await get_random_cart("action_cart", used_carts)

    used_carts += [
        profession.pk,
        personality.pk,
        hobby.pk,
        information.pk,
        item.pk,
        action_two.pk,
    ]

    if good_health:
        health = await Cart.objects.aget(name="Полностью Здоров.")
    else:
        health = await get_random_cart("health_cart", used_carts)
        used_carts.append(health.pk)
    if no_phobia:
        phobia = await Cart.objects.aget(name="Отсутствует")
    else:
        phobia = await get_random_cart("phobia_cart", used_carts)
        used_carts.append(phobia.pk)
    if getero_orientation:
        orientation = await Cart.objects.aget(name="Гетеросексуал")
    else:
        orientation = await get_random_cart("orientation_cart")

    return (
        await Character.objects.acreate(
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
        ),
        used_carts,
    )


async def generate_characters(users, game):
    """Метод получения уникальных персонажей."""
    unique_cart_data = []
    for user in users:
        character, unique_cart_data = await generate_character(
            user, game, unique_cart_data
        )
