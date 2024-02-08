from aiogram.utils.keyboard import InlineKeyboardBuilder
from game.models import Character, Game

from bot.constants import buttons
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
                action=action_cart_action.get, id=cart.id
            ),
        )
    keyboard = await back_builder(keyboard, game_action.get_epidemia)
    keyboard.adjust(1)
    return keyboard


async def not_active_cart_keyboard():
    """Клавиатура не активной карты."""
    keyboard = InlineKeyboardBuilder()
    keyboard = await back_builder(keyboard, action_cart_action.list)
    return keyboard


async def cart_confirmation_keyboard(callback_data: ActionCartCallbackData):
    """Клавиатура подстверждения использования карты."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=buttons.YES_BUTTON,
        callback_data=ActionCartCallbackData(
            action=action_cart_action.use_cart,
            id=callback_data.id,
        ),
    )
    keyboard.button(
        text=buttons.NO_BUTTON,
        callback_data=ActionCartCallbackData(action=action_cart_action.list),
    )
    keyboard.adjust(1)
    return keyboard


async def choose_target_keyboard(
    callback_data: ActionCartCallbackData, game: Game
):
    """Клавиатура режима игры в одном сообщении."""
    keyboard = InlineKeyboardBuilder()
    async for user in game.users.all():
        keyboard.button(
            text=user.full_name,
            callback_data=ActionCartCallbackData(
                action=action_cart_action.choose_target,
                id=callback_data.id,
                target=user.telegram_id,
            ),
        )
    keyboard = await back_builder(keyboard, action_cart_action.list)
    keyboard.adjust(1)
    return keyboard
