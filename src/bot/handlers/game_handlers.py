from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from game.models import TypeInformationCarts
from game.utils.character import get_character, get_character_info_text
from game.utils.game import (
    close_game,
    get_bunker_info_text,
    get_players_in_game_message,
    start_game,
)

from bot.constants import messages
from bot.constants.actions import game_action
from bot.constants.callback_data import GameCallbackData
from bot.keyboards.inline_keyboards import (
    game_all_info_keyboard,
    game_keyboard,
    game_settings_keyboard,
    room_keyboard,
)
from bot.models import User
from bot.utils.user_helpers import get_user
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
    if not user.room:
        await callback.message.edit_text(text=messages.NOT_IN_ROOM_MESSAGE)
        return
    if user.game:
        await callback.message.delete()
        return
    text, started = await start_game(user.room)
    if not started:
        await callback.message.answer(text=text)
        return
    await callback.message.delete()
    async for player in (
        User.objects.select_related("room__admin", "game")
        .filter(room=user.room)
        .all()
    ):
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
    if not user.game:
        await callback.message.edit_text(text=messages.NO_GAME_MESSAGE)
        return
    character = await get_character(user)
    keyboard = await game_keyboard(user, callback_data=callback_data)
    await callback.message.edit_text(
        text=await get_character_info_text(character),
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
    user = await User.objects.select_related("game", "room__admin").aget(
        telegram_id=callback.from_user.id
    )
    if not user.game:
        await callback.message.edit_text(text=messages.NO_GAME_MESSAGE)
        return
    keyboard = await game_keyboard(user, callback_data=callback_data)
    await callback.message.edit_text(
        text=messages.EPIDEMIA_GET_MESSAGE.format(
            await user.game.information_carts.filter(
                type=TypeInformationCarts.EPIDEMIA
            ).alast(),
            user.game.epidemia_time,
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
        "game",
        "room__admin",
    ).aget(telegram_id=callback.from_user.id)
    if not user.game:
        await callback.message.edit_text(text=messages.NO_GAME_MESSAGE)
        return
    keyboard = await game_keyboard(user, callback_data=callback_data)
    await callback.message.edit_text(
        text=await get_bunker_info_text(user.game),
        reply_markup=keyboard.as_markup(),
    )


@router.callback_query(
    GameCallbackData.filter(F.action == game_action.get_all_info)
)
@log_in_dev
async def get_all_info_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: GameCallbackData,
):
    """Хендлер просмотра всей информации."""
    user = await User.objects.select_related(
        "game",
        "room__admin",
    ).aget(telegram_id=callback.from_user.id)
    if not user.game:
        await callback.message.edit_text(text=messages.NO_GAME_MESSAGE)
        return
    text = "<b>Эпидемия:</b>\n"
    text += messages.EPIDEMIA_GET_MESSAGE.format(
        await user.game.information_carts.filter(
            type=TypeInformationCarts.EPIDEMIA
        ).alast(),
        user.game.epidemia_time,
    )
    text += "\n\n<b>Бункер:</b>\n"
    text += await get_bunker_info_text(user.game)
    text += "\n<b>Персонаж:</b>\n"
    character = await get_character(user)
    text += await get_character_info_text(character)
    keyboard = await game_all_info_keyboard(user, callback_data=callback_data)
    await callback.message.edit_text(
        text=text,
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
    if not user.game:
        await callback.message.edit_text(text=messages.NO_GAME_MESSAGE)
        return
    text = await get_players_in_game_message(user.game)
    keyboard = await game_settings_keyboard(user)
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
    if not user.game:
        await callback.message.edit_text(text=messages.NO_GAME_MESSAGE)
        return
    await close_game(user.game)
    text, started = await start_game(user.room)
    if not started:
        await callback.answer(text=text)
        return
    await callback.message.delete()
    async for player in (
        User.objects.select_related("game", "room", "room__admin")
        .filter(room=user.room)
        .all()
    ):
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
    await callback.message.delete()
    if not user.game:
        await callback.message.edit_text(text=messages.NO_GAME_MESSAGE)
        return
    await close_game(user.game)
    user.room.started = False
    await user.room.asave(update_fields=("started",))
    await User.objects.filter(game=user.game).aupdate(game=None)
    async for player in (
        User.objects.select_related("room__admin").filter(room=user.room).all()
    ):
        keyboard = await room_keyboard(player)
        await callback.bot.send_message(
            chat_id=player.telegram_id,
            text=messages.GAME_CLOSED_MESSAGE,
            reply_markup=keyboard.as_markup(),
        )
