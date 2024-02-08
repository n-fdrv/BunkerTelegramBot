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


async def regenerate_cart(cart: ActionCart, target: list[Character]):
    """Метод перегенерирования карты."""
    not_cart_data = [ValueAction.AGE, ValueAction.BUNKER_SUPPLY]
    not_unique_cart_data = {
        ValueAction.GENDER: TypeInformationCarts.GENDER,
        ValueAction.ORIENTATION: TypeInformationCarts.ORIENTATION,
    }
    cart_data = {
        ValueAction.EPIDEMIA: TypeInformationCarts.EPIDEMIA,
        ValueAction.BUNKER_TYPE: TypeInformationCarts.BUNKER_TYPE,
        ValueAction.BUNKER_ROOM: TypeInformationCarts.BUNKER_ROOM,
        ValueAction.PROFESSION: TypeInformationCarts.PROFESSION,
        ValueAction.HEALTH: TypeInformationCarts.HEALTH,
        ValueAction.PHOBIA: TypeInformationCarts.PHOBIA,
        ValueAction.PERSONALITY: TypeInformationCarts.PERSONALITY,
        ValueAction.HOBBY: TypeInformationCarts.HOBBY,
        ValueAction.ADDITIONAL_INFO: TypeInformationCarts.ADDITIONAL_INFO,
        ValueAction.ITEM: TypeInformationCarts.ITEM,
    }
    for character in target:
        if cart.value in not_cart_data:
            print("not_cart")
            return
        elif cart.value in not_unique_cart_data:
            print("not unique")
            return
        new_info_cart = await get_random_unique_information_cart(
            cart_type=cart_data[cart.value], game=character.game
        )
        old_info_cart = await character.information_carts.filter(
            type=cart_data[cart.value]
        ).alast()
        await character.information_carts.aremove(old_info_cart)
        await character.information_carts.aadd(new_info_cart)
        character_action_cart = await ActionCharacter.objects.filter(
            cart=cart, character=character
        ).alast()
        character_action_cart.is_used = True
        await character_action_cart.asave(update_fields=("is_used",))
        return new_info_cart


async def use_action_cart(cart: ActionCart, target: list[Character]):
    """Распределение карт по функциям."""
    cart_def_data = {KeyAction.GENERATE: regenerate_cart}

    return await cart_def_data[cart.key](cart, target)
