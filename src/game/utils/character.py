from random import randint

from django.conf import settings

from game.models import Character, Game, InformationCart, TypeInformationCarts
from game.utils.cart import (
    get_random_action_cart,
    get_random_information_cart,
    get_random_unique_information_cart,
)

from bot.constants.messages import CHARACTER_GET_MESSAGE
from bot.models import User


async def create_character(user: User, game: Game):
    """Метод генерации случайного персонажа."""
    age = randint(settings.AVERAGE_AGE_VALUE, settings.MAX_AGE_VALUE)
    gender = await get_random_information_cart(TypeInformationCarts.GENDER)
    profession = await get_random_unique_information_cart(
        TypeInformationCarts.PROFESSION, game
    )
    personality = await get_random_unique_information_cart(
        TypeInformationCarts.PERSONALITY, game
    )
    hobby = await get_random_unique_information_cart(
        TypeInformationCarts.HOBBY, game
    )
    information = await get_random_unique_information_cart(
        TypeInformationCarts.ADDITIONAL_INFO, game
    )
    item = await get_random_unique_information_cart(
        TypeInformationCarts.ITEM, game
    )
    action_one = await get_random_action_cart()
    action_two = await get_random_action_cart()

    if randint(1, 100) <= settings.HEALTH_CHANCE:
        health = await InformationCart.objects.aget(name="Полностью Здоров.")
    else:
        health = await get_random_unique_information_cart(
            TypeInformationCarts.HEALTH, game
        )

    if randint(1, 100) <= settings.PHOBIA_CHANCE:
        phobia = await InformationCart.objects.aget(name="Отсутствует")
    else:
        phobia = await get_random_unique_information_cart(
            TypeInformationCarts.PHOBIA, game
        )

    if randint(1, 100) <= settings.ORIENTATION_CHANCE:
        orientation = await InformationCart.objects.aget(name="Гетеросексуал")
    else:
        orientation = await get_random_unique_information_cart(
            TypeInformationCarts.ORIENTATION, game
        )
    if randint(1, 100) <= settings.YOUNG_AGE_CHANCE:
        age = randint(settings.MIN_AGE_VALUE, settings.AVERAGE_AGE_VALUE)

    character = await Character.objects.acreate(user=user, age=age, game=game)
    await character.information_carts.aadd(
        gender,
        profession,
        personality,
        hobby,
        information,
        item,
        health,
        phobia,
        orientation,
    )
    await character.action_carts.aadd(action_one, action_two)
    return character


async def get_character(user: User) -> Character:
    """Метод получения персонажа из базы данных."""
    return await Character.objects.aget(user=user, game=user.game)


async def get_info_cart_text(character: Character, cart_type):
    """Метод получения текста информационных карт."""
    text = ""
    async for info in character.information_carts.filter(type=cart_type):
        text += f"{info} "
    return text


async def get_action_cart_text(character: Character):
    """Метод получения текста карт действий."""
    action_text = ""
    action_number = 1
    async for action in character.action_carts.all():
        action_text += f"<b>{action_number}. {action}</b>\n"
        action_number += 1
    return action_text


async def get_character_info_text(character: Character) -> str:
    """Метод получения информации о персонаже."""
    text = CHARACTER_GET_MESSAGE.format(
        await get_info_cart_text(character, TypeInformationCarts.PROFESSION),
        await character.information_carts.aget(
            type=TypeInformationCarts.GENDER
        ),
        character.age,
        await character.information_carts.aget(
            type=TypeInformationCarts.ORIENTATION
        ),
        await get_info_cart_text(character, TypeInformationCarts.HEALTH),
        await get_info_cart_text(character, TypeInformationCarts.PHOBIA),
        await get_info_cart_text(character, TypeInformationCarts.HOBBY),
        await get_info_cart_text(character, TypeInformationCarts.PERSONALITY),
        await get_info_cart_text(
            character, TypeInformationCarts.ADDITIONAL_INFO
        ),
        await get_info_cart_text(character, TypeInformationCarts.ITEM),
        await get_action_cart_text(character),
    )
    return text
