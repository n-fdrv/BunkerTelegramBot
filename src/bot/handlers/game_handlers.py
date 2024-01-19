from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.constants import messages
from bot.constants.actions import game_action
from bot.constants.callback_data import GameCallbackData
from bot.constants.messages import CHARACTER_GET_MESSAGE
from bot.keyboards.inline_keyboards import (
    game_keyboard,
    game_settings_keyboard,
)
from bot.models import User
from bot.utils.game_helpers import get_players_in_game_message, start_game
from bot.utils.state_helpers import get_character, get_user
from core.config.logging import log_in_dev

router = Router()


@router.callback_query(GameCallbackData.filter(F.action == game_action.start))
@log_in_dev
async def start_game_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: GameCallbackData,
):
    """Хендлер начала игры."""
    user = await get_user(callback.from_user.id)
    text, started = await start_game(user.room)
    if not started:
        await callback.message.answer(text=text)
        return
    await callback.message.delete()
    async for player in User.objects.select_related(
        "room__admin", "game"
    ).filter(room=user.room).all():
        keyboard = await game_keyboard(player, callback_data=callback_data)
        await callback.message.bot.send_message(
            chat_id=player.telegram_id,
            text=messages.GAME_STARTED_MESSAGE,
            reply_markup=keyboard.as_markup(),
        )


@router.callback_query(
    GameCallbackData.filter(F.action == game_action.get_character)
)
@log_in_dev
async def get_character_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: GameCallbackData,
):
    """Хендлер просмотра персонажа."""
    user = await get_user(callback.from_user.id)
    character = await get_character(user)
    keyboard = await game_keyboard(user, callback_data=callback_data)
    await callback.message.edit_text(
        text=CHARACTER_GET_MESSAGE.format(
            character.profession,
            character.gender,
            character.age,
            character.orientation,
            character.health,
            character.phobia,
            character.hobby,
            character.personality,
            character.information,
            character.item,
            character.action_one,
            character.action_two,
        ),
        reply_markup=keyboard.as_markup(),
    )


@router.callback_query(
    GameCallbackData.filter(F.action == game_action.get_epidemia)
)
@log_in_dev
async def get_epidemia_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: GameCallbackData,
):
    """Хендлер просмотра информации о катастрофе."""
    user = await User.objects.select_related(
        "game__epidemia", "room__admin"
    ).aget(telegram_id=callback.from_user.id)
    keyboard = await game_keyboard(user, callback_data=callback_data)
    await callback.message.edit_text(
        text=messages.EPIDEMIA_GET_MESSAGE.format(
            user.game.epidemia, user.game.epidemia_time
        ),
        reply_markup=keyboard.as_markup(),
    )


@router.callback_query(
    GameCallbackData.filter(F.action == game_action.get_bunker)
)
@log_in_dev
async def get_bunker_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: GameCallbackData,
):
    """Хендлер просмотра информации о бункере."""
    user = await User.objects.select_related(
        "game__bunker_type",
        "game__room_one",
        "game__room_two",
        "game__room_three",
        "room__admin",
    ).aget(telegram_id=callback.from_user.id)
    keyboard = await game_keyboard(user, callback_data=callback_data)
    await callback.message.edit_text(
        text=messages.BUNKER_GET_MESSAGE.format(
            user.game.bunker_type,
            user.game.bunker_place_amount,
            user.game.room_one,
            user.game.room_two,
            user.game.room_three,
        ),
        reply_markup=keyboard.as_markup(),
    )


@router.callback_query(
    GameCallbackData.filter(F.action == game_action.game_settings)
)
@log_in_dev
async def get_game_settings_handler(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: GameCallbackData,
):
    """Хендлер настроек игры."""
    user = await get_user(callback.from_user.id)
    text = await get_players_in_game_message(user.game)
    keyboard = await game_settings_keyboard()
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard.as_markup(),
        parse_mode="Markdown",
    )


@router.callback_query(
    GameCallbackData.filter(F.action == game_action.reload_game)
)
@log_in_dev
async def reload_game_handler(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: GameCallbackData,
):
    """Хендлер перезапуска игры."""
    user = await get_user(callback.from_user.id)
    user.game.is_closed = True
    await user.game.asave(update_fields=("is_closed",))
    text, started = await start_game(user.room)
    if not started:
        await callback.answer(text=text)
        return
    await callback.message.delete()
    async for player in User.objects.select_related(
        "game", "room", "room__admin"
    ).filter(room=user.room).all():
        keyboard = await game_keyboard(player)
        await callback.bot.send_message(
            chat_id=player.telegram_id,
            text=messages.GAME_STARTED_MESSAGE,
            reply_markup=keyboard.as_markup(),
        )


@router.callback_query(
    GameCallbackData.filter(F.action == game_action.close_game)
)
@log_in_dev
async def close_game_handler(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: GameCallbackData,
):
    """Хендлер закрытия игры и перехода в лобби."""
    user = await get_user(callback.from_user.id)
    user.game.is_closed = True
    user.room.started = False
    await user.room.asave(update_fields=("started",))
    await user.game.asave(update_fields=("is_closed",))
    await callback.message.delete()
    await User.objects.filter(game=user.game).aupdate(game=None)
    async for player in User.objects.filter(room=user.room).all():
        await callback.bot.send_message(
            chat_id=player.telegram_id,
            text=messages.GAME_CLOSED_MESSAGE,
        )
