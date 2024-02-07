from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.constants import messages
from bot.constants.actions import start_action
from bot.constants.callback_data import StartCallbackData
from bot.keyboards.inline_keyboards import (
    about_keyboard,
    help_keyboard,
    rules_keyboard,
    start_keyboard,
)
from core.config.logging import log_in_dev

router = Router()


@router.callback_query(StartCallbackData.filter(F.action == start_action.get))
@log_in_dev
async def start_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: StartCallbackData,
):
    """Хендлер помощи."""
    keyboard = await start_keyboard()
    await callback.message.edit_text(
        text=messages.START_MESSAGE, reply_markup=keyboard.as_markup()
    )


@router.callback_query(
    StartCallbackData.filter(F.action == start_action.about)
)
@log_in_dev
async def help_handler(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: StartCallbackData,
):
    """Хендлер помощи."""
    keyboard = await about_keyboard(callback_data.page)
    await callback.message.edit_text(
        text=messages.ABOUT_MESSAGE[callback_data.page - 1],
        reply_markup=keyboard.as_markup(),
    )


@router.callback_query(
    StartCallbackData.filter(F.action == start_action.rules)
)
@log_in_dev
async def rules_handler(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: StartCallbackData,
):
    """Хендлер помощи."""
    keyboard = await rules_keyboard(callback_data.page)
    await callback.message.edit_text(
        text=messages.RULES_MESSAGE[callback_data.page - 1],
        reply_markup=keyboard.as_markup(),
    )


@router.callback_query(StartCallbackData.filter(F.action == start_action.help))
@log_in_dev
async def help_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: StartCallbackData,
):
    """Хендлер помощи."""
    keyboard = await help_keyboard()
    await callback.message.edit_text(
        text=messages.HELP_MESSAGE, reply_markup=keyboard.as_markup()
    )
