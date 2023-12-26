from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.constants.actions import room_action
from bot.constants.callback_data import RoomCallbackData
from bot.constants.messages import (
    CHARACTER_GET_MESSAGE,
    NO_ROOM_MESSAGE,
    START_MESSAGE,
    USER_ENTERED_ROOM_ADMIN_MESSAGE,
    USER_ENTERED_ROOM_MESSAGE,
    USER_LEAVE_ROOM_MESSAGE,
)
from bot.constants.states import RoomState
from bot.keyboards import inline_keyboards
from bot.keyboards.inline_keyboards import cancel_state_keyboard
from bot.models import User
from bot.utils.character_generator import generate_character
from bot.utils.room_helpers import get_room
from bot.utils.user_helpers import get_user_url
from core.config.logging import log_in_dev

router = Router()


@router.message(RoomState.enter_room_slug)
@log_in_dev
async def enter_room_slug_handler(message: types.Message, state: FSMContext):
    """Хендлер проверки и входа в комнату."""
    keyboard = await cancel_state_keyboard()
    room = await get_room(message.text)
    if not room:
        await state.set_state(RoomState.enter_room_slug)
        await message.answer(
            text=NO_ROOM_MESSAGE, reply_markup=keyboard.as_markup()
        )
        return
    user = await User.objects.aget(telegram_id=message.from_user.id)
    user.room = room
    await user.asave(update_fields=("room",))
    await message.answer(
        text=USER_ENTERED_ROOM_MESSAGE, reply_markup=keyboard.as_markup()
    )
    admin_keyboard = await inline_keyboards.room_admin_keyboard(room)
    await message.bot.send_message(
        chat_id=room.admin.telegram_id,
        text=USER_ENTERED_ROOM_ADMIN_MESSAGE.format(get_user_url(user)),
        reply_markup=admin_keyboard.as_markup(),
        parse_mode="Markdown",
    )
    await state.clear()


@router.callback_query(RoomCallbackData.filter(F.action == room_action.cancel))
@log_in_dev
async def cancel_enter_room_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: RoomCallbackData,
):
    """Хендлер отмены состояния и выхода из комнаты."""
    await state.clear()
    user = await User.objects.select_related("room").aget(
        telegram_id=callback.from_user.id
    )
    if user.room:
        user.room = None
        await user.asave(update_fields=("room",))
        await callback.message.edit_text(
            text=USER_LEAVE_ROOM_MESSAGE,
        )
        return
    await callback.message.edit_text(text=START_MESSAGE)


@router.callback_query(
    RoomCallbackData.filter(F.action == room_action.players)
)
@log_in_dev
async def show_players_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: RoomCallbackData,
):
    """Хендлер просмотра игроков в комнате."""
    user = await User.objects.select_related("room", "room__admin").aget(
        telegram_id=callback.from_user.id
    )
    keyboard = await inline_keyboards.show_players_keyboard(user.room)
    await callback.message.edit_reply_markup(reply_markup=keyboard.as_markup())


@router.callback_query(
    RoomCallbackData.filter(F.action == room_action.admin_get)
)
@log_in_dev
async def show_room_admin_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: RoomCallbackData,
):
    """Хендлер просмотра комнаты администратором."""
    user = await User.objects.select_related("room", "room__admin").aget(
        telegram_id=callback.from_user.id
    )
    keyboard = await inline_keyboards.room_admin_keyboard(user.room)
    await callback.message.edit_reply_markup(
        text=f"Комната №{user.room.slug}", reply_markup=keyboard.as_markup()
    )


@router.callback_query(RoomCallbackData.filter(F.action == room_action.begin))
@log_in_dev
async def begin_game_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: RoomCallbackData,
):
    """Хендлер просмотра комнаты администратором."""
    user = await User.objects.select_related("room", "room__admin").aget(
        telegram_id=callback.from_user.id
    )
    character = await generate_character(user)
    await callback.message.answer(
        text=CHARACTER_GET_MESSAGE.format(
            character.profession,
            character.gender,
            character.orientation,
            character.age,
            character.health,
            character.phobia,
            character.hobby,
            character.personality,
            character.information,
            character.item,
            character.action_one,
            character.action_two,
        )
    )
