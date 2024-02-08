from aiogram.utils.keyboard import InlineKeyboardBuilder
from game.models import Character

from bot.constants.actions import action_cart_action, game_action
from bot.constants.callback_data import (
    ActionCartCallbackData,
)
from bot.utils.back_button_builder import back_builder


async def action_list_keyboard(character: Character):
    """Клавиатура режима игры в одном сообщении."""
    keyboard = InlineKeyboardBuilder()
    async for cart in character.action_carts.all():
        keyboard.button(
            text=cart.name,
            callback_data=ActionCartCallbackData(
                action=action_cart_action.get,
                key=cart.key,
                target=cart.target,
                value=cart.value,
            ),
        )
    keyboard = await back_builder(keyboard, game_action.get_epidemia)
    keyboard.adjust(1)
    return keyboard
