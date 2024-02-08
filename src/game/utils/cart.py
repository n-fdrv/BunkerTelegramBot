from random import randint

from django.conf import settings

from game.models import (
    ActionCart,
    ActionCharacter,
    Character,
    Game,
    InformationCart,
    KeyAction,
    TypeInformationCarts,
    ValueAction,
)


async def get_random_information_cart(cart_type) -> InformationCart:
    """Метод получения случайной карты информации."""
    return (
        await InformationCart.objects.filter(type=cart_type)
        .order_by("?")
        .afirst()
    )


async def get_random_unique_information_cart(
    cart_type, game: Game
) -> InformationCart:
    """Метод получения уникальной случайной карты информации."""
    cart = (
        await InformationCart.objects.filter(type=cart_type)
        .order_by("?")
        .exclude(pk__in=game.unique_carts.values_list("id", flat=True))
        .afirst()
    )
    await game.unique_carts.aadd(cart)
    return cart


async def get_random_action_cart() -> ActionCart:
    """Метод получения случайной карты действия."""
    return await ActionCart.objects.order_by("?").afirst()


async def check_is_used_cart(character: Character, cart: ActionCart) -> bool:
    """Проверка была ли использована карта."""
    character_action_cart = await ActionCharacter.objects.filter(
        cart=cart, character=character
    ).alast()
    return character_action_cart.is_used


async def generate_age() -> int:
    """Метод генерации случайного возраста."""
    age = randint(settings.AVERAGE_AGE_VALUE, settings.MAX_AGE_VALUE)

    if randint(1, 100) <= settings.YOUNG_AGE_CHANCE:
        age = randint(settings.MIN_AGE_VALUE, settings.AVERAGE_AGE_VALUE)

    return age


async def regenerate_cart(
    character_action: ActionCharacter, target: list[Character]
):
    """Метод перегенерации карты."""
    cart_data = {
        ValueAction.PROFESSION: TypeInformationCarts.PROFESSION,
        ValueAction.HEALTH: TypeInformationCarts.HEALTH,
        ValueAction.PHOBIA: TypeInformationCarts.PHOBIA,
        ValueAction.PERSONALITY: TypeInformationCarts.PERSONALITY,
        ValueAction.HOBBY: TypeInformationCarts.HOBBY,
        ValueAction.ADDITIONAL_INFO: TypeInformationCarts.ADDITIONAL_INFO,
        ValueAction.ITEM: TypeInformationCarts.ITEM,
    }
    not_unique_cart_data = {
        ValueAction.GENDER: TypeInformationCarts.GENDER,
        ValueAction.ORIENTATION: TypeInformationCarts.ORIENTATION,
    }
    if character_action.cart.value in cart_data:
        cart_type = cart_data[character_action.cart.value]
    else:
        cart_type = not_unique_cart_data[character_action.cart.value]
    for character in target:
        new_info_cart = await get_random_unique_information_cart(
            cart_type=cart_type, game=character.game
        )
        old_info_cart = await character.information_carts.filter(
            type=cart_type
        ).alast()
        await character.information_carts.aremove(old_info_cart)
        await character.information_carts.aadd(new_info_cart)


async def regenerate_int(
    character_action: ActionCharacter, target: list[Character]
):
    """Метод перегенерирования числового значения."""
    if character_action.cart.value == ValueAction.AGE:
        for character in target:
            character.age = await generate_age()
            await character.asave(update_fields=("age",))
    else:
        for character in target:
            character.game.epidemia_time = randint(1, 10)
            await character.game.asave(update_fields=("epidemia_time",))


async def regenerate_bunker_cart(
    character_action: ActionCharacter, target: list[Character]
):
    """Метод перегенерирования карты бункера."""
    cart_data = {
        ValueAction.EPIDEMIA: TypeInformationCarts.EPIDEMIA,
        ValueAction.BUNKER_TYPE: TypeInformationCarts.BUNKER_TYPE,
    }
    game = character_action.character.game
    cart_type = cart_data[character_action.cart.value]
    new_info_cart = await get_random_unique_information_cart(
        cart_type=cart_type, game=game
    )
    old_info_cart = await game.information_carts.filter(type=cart_type).alast()
    await game.information_carts.aremove(old_info_cart)
    await game.information_carts.aadd(new_info_cart)


async def use_action_cart(
    character_action: ActionCharacter, target: list[Character]
):
    """Распределение карт по функциям."""
    cart_def_data = {
        KeyAction.GENERATE_INT: regenerate_int,
        KeyAction.GENERATE_CART: regenerate_cart,
        KeyAction.GENERATE_BUNKER_CART: regenerate_bunker_cart,
    }
    character_action.is_used = True
    await character_action.asave(update_fields=("is_used",))
    return await cart_def_data[character_action.cart.key](
        character_action, target
    )
