from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from game.utils.character import get_character

from bot.constants.actions import action_cart_action
from bot.constants.callback_data import ActionCartCallbackData
from bot.constants.messages_data import action_messages
from bot.keyboards import action_keyboards
from bot.utils.user_helpers import get_user
from core.config.logging import log_in_dev

router = Router()


@router.callback_query(
    ActionCartCallbackData.filter(F.action == action_cart_action.list)
)
@log_in_dev
async def action_list(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: ActionCartCallbackData,
):
    """Хендлер начала игры."""
    user = await get_user(callback.from_user.id)
    character = await get_character(user)
    keyboard = await action_keyboards.action_list_keyboard(character)
    await callback.message.edit_text(
        text=action_messages.LIST_MESSAGE, reply_markup=keyboard.as_markup()
    )
