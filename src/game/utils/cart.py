from game.models import ActionCart, Game, InformationCart


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
