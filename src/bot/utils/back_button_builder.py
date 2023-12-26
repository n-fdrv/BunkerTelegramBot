from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.constants import buttons
from bot.utils.callback_helpers import get_callback_by_action


async def back_builder(
    keyboard: InlineKeyboardBuilder,
    action,
    item_id: int = None,
    page: int = None,
    **kwargs
) -> InlineKeyboardBuilder:
    """Добавляет кнопку назад в inline-клавиатуру."""
    callback = get_callback_by_action(action)
    if item_id:
        callback.id = item_id
    if "user_id" in kwargs:
        callback.user_id = kwargs["user_id"]
    if "order_status" in kwargs:
        callback.order_status = kwargs["order_status"]
    if page:
        callback.page = page
    keyboard.button(text=buttons.BACK_BUTTON, callback_data=callback)
    return keyboard
