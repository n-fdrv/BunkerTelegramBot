from random import randint

from django.conf import settings

from bot.models import Cart, Character, User


async def generate_character(user: User):
    """Метод генерации случайного персонажа."""
    good_health = randint(1, 100) <= settings.HEALTH_CHANCE
    no_phobia = randint(1, 100) <= settings.PHOBIA_CHANCE
    getero_orientation = randint(1, 100) < settings.ORIENTATION_CHANCE
    age = randint(settings.MIN_AGE_VALUE, settings.MAX_AGE_VALUE)

    gender = (
        await Cart.objects.filter(type="gender_cart").order_by("?").afirst()
    )
    orientation = (
        await Cart.objects.filter(type="orientation_cart")
        .order_by("?")
        .afirst()
    )
    profession = (
        await Cart.objects.filter(type="prof_cart").order_by("?").afirst()
    )
    health = (
        await Cart.objects.filter(type="health_cart").order_by("?").afirst()
    )
    phobia = (
        await Cart.objects.filter(type="phobia_cart").order_by("?").afirst()
    )
    personality = (
        await Cart.objects.filter(type="personality_cart")
        .order_by("?")
        .afirst()
    )
    hobby = await Cart.objects.filter(type="hobby_cart").order_by("?").afirst()
    information = (
        await Cart.objects.filter(type="ad_info_cart").order_by("?").afirst()
    )
    item = await Cart.objects.filter(type="item_cart").order_by("?").afirst()
    action_one = (
        await Cart.objects.filter(type="action_cart").order_by("?").afirst()
    )
    action_two = (
        await Cart.objects.filter(type="action_cart").order_by("?").afirst()
    )

    if good_health:
        health = await Cart.objects.aget(name="Полностью здоров.")
    if no_phobia:
        phobia = await Cart.objects.aget(name="Отсутствует")
    if getero_orientation:
        orientation = await Cart.objects.aget(name="Гетеросексуал")

    return await Character.objects.acreate(
        user=user,
        room=user.room,
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
    )
