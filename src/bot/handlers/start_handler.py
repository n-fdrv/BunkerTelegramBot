from aiogram import F, Router, types
from aiogram.filters import KICKED, ChatMemberUpdatedFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatMemberUpdated

from bot.constants.actions import room_action
from bot.constants.callback_data import RoomCallbackData
from bot.constants.messages import (
    CHARACTER_GET_MESSAGE,
    CREATE_ROOM_MESSAGE,
    ENTER_ROOM_SLUG_MESSAGE,
    NO_ROOM_MESSAGE,
    NOT_CREATED_ROOM_MESSAGE,
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
from bot.utils.room_helpers import create_room, get_room
from bot.utils.user_helpers import get_user_url
from core.config.logging import log_in_dev

router = Router()


@router.message(Command("start"))
@log_in_dev
async def start_handler(message: types.Message, state: FSMContext):
    """Хендлер при нажатии кнопки start."""
    user, created = await User.objects.aget_or_create(
        telegram_id=message.from_user.id,
    )
    user.first_name = message.from_user.first_name
    user.last_name = message.from_user.last_name
    user.telegram_username = message.from_user.username
    await user.asave()
    keyboard = await inline_keyboards.start_keyboard()
    await message.answer(text=START_MESSAGE, reply_markup=keyboard.as_markup())


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
@log_in_dev
async def block_handler(event: ChatMemberUpdated, state: FSMContext):
    """Хендлер при блокировке бота."""
    user = await User.objects.aget(telegram_id=event.from_user.id)
    await user.adelete()


@router.message(Command("new_room"))
@log_in_dev
async def create_room_handler(message: types.Message, state: FSMContext):
    """Хендлер при нажатии кнопки start."""
    user = await User.objects.select_related("room").aget(
        telegram_id=message.from_user.id
    )
    room, created = await create_room(user)
    if not created:
        await message.answer(text=NOT_CREATED_ROOM_MESSAGE.format(room.slug))
        return
    await message.answer(text=CREATE_ROOM_MESSAGE.format(room.slug))


@router.callback_query(RoomCallbackData.filter(F.action == room_action.create))
@log_in_dev
async def create_room_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: RoomCallbackData,
):
    """Хендлер Создания комнаты."""
    user = await User.objects.select_related("room").aget(
        telegram_id=callback.from_user.id
    )
    room, created = await create_room(user)
    if not created:
        await callback.message.edit_text(
            text=NOT_CREATED_ROOM_MESSAGE.format(room.slug)
        )
        return
    await callback.message.edit_text(
        text=CREATE_ROOM_MESSAGE.format(room.slug)
    )


@router.callback_query(RoomCallbackData.filter(F.action == room_action.enter))
@log_in_dev
async def enter_room_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: RoomCallbackData,
):
    """Хендлер перехода в состояние входа в комнату."""
    await state.set_state(RoomState.enter_room_slug)
    keyboard = await cancel_state_keyboard()
    await callback.message.edit_text(
        text=ENTER_ROOM_SLUG_MESSAGE, reply_markup=keyboard.as_markup()
    )


@router.message(RoomState.enter_room_slug)
@log_in_dev
async def enter_room_slug_handler(message: types.Message, state: FSMContext):
    """Хендлер проверки и входа в комнату."""
    keyboard = await cancel_state_keyboard()
    if not message.text.isdigit():
        await state.set_state(RoomState.enter_room_slug)
        await message.answer(
            text=NO_ROOM_MESSAGE, reply_markup=keyboard.as_markup()
        )
        return
    room_slug = int(message.text)
    room = await get_room(room_slug)
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
    keyboard = await inline_keyboards.start_keyboard()
    await callback.message.edit_text(
        text=START_MESSAGE, reply_markup=keyboard.as_markup()
    )


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


@router.message(Command("my_room"))
@log_in_dev
async def show_room_admin_command(message: types.Message, state: FSMContext):
    """Хендлер просмотра комнаты администратором."""
    user = await User.objects.select_related("room", "room__admin").aget(
        telegram_id=message.from_user.id
    )
    keyboard = await inline_keyboards.room_admin_keyboard(user.room)
    await message.answer(
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
