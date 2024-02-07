from aiogram import Router, types
from aiogram.filters import KICKED, ChatMemberUpdatedFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatMemberUpdated

from bot.constants import commands
from bot.constants.messages import (
    CREATE_ROOM_MESSAGE,
    ENTER_ROOM_SLUG_MESSAGE,
    GAME_STARTED_MESSAGE,
    HELP_MESSAGE,
    NOT_CREATED_ROOM_MESSAGE,
    NOT_IN_ROOM_MESSAGE,
    PLAYER_LEFT_ROOM_MESSAGE,
    ROOM_IS_CLOSED_MESSAGE,
    RULES_MESSAGE,
    RULES_MESSAGE_2,
    START_MESSAGE,
    USER_CANT_ENTER_ROOM,
    YOU_LEFT_ROOM_MESSAGE,
)
from bot.constants.states import RoomState
from bot.keyboards import inline_keyboards
from bot.keyboards.inline_keyboards import cancel_state_keyboard, game_keyboard
from bot.models import User
from bot.utils.room_helpers import create_room, get_players_in_room_message
from bot.utils.user_helpers import get_user, get_user_url
from core.config.logging import log_in_dev

router = Router()


@router.message(Command(commands.START_COMMAND))
@log_in_dev
async def start_handler(message: types.Message, state: FSMContext):
    """Хендлер при нажатии кнопки start."""
    await state.clear()
    user, created = await User.objects.aget_or_create(
        telegram_id=message.from_user.id,
    )
    user.first_name = message.from_user.first_name
    user.last_name = message.from_user.last_name
    user.telegram_username = message.from_user.username
    await user.asave()
    await message.answer(text=START_MESSAGE)


@router.message(Command(commands.HELP_COMMAND))
@log_in_dev
async def help_handler(message: types.Message, state: FSMContext):
    """Хендлер команды help."""
    await message.answer(text=HELP_MESSAGE)


@router.message(Command(commands.RULES_COMMAND))
@log_in_dev
async def rules_handler(message: types.Message, state: FSMContext):
    """Хендлер команды rules."""
    await message.answer(text=RULES_MESSAGE)
    await message.answer(text=RULES_MESSAGE_2)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
@log_in_dev
async def block_handler(event: ChatMemberUpdated, state: FSMContext):
    """Хендлер при блокировке бота."""
    await state.clear()
    user = await get_user(event.from_user.id)
    await user.adelete()


@router.message(Command(commands.NEW_GAME_ROOM_COMMAND))
@log_in_dev
async def create_room_handler(message: types.Message, state: FSMContext):
    """Хендлер создания лобби."""
    await state.clear()
    user = await get_user(message.from_user.id)
    room, created = await create_room(user)
    if not created:
        await message.answer(text=NOT_CREATED_ROOM_MESSAGE.format(room.slug))
        return
    await message.answer(text=CREATE_ROOM_MESSAGE.format(room.slug))


@router.message(Command(commands.MY_GAME_ROOM_COMMAND))
@log_in_dev
async def show_room_command(message: types.Message, state: FSMContext):
    """Хендлер просмотра комнаты."""
    await state.clear()
    user = await get_user(message.from_user.id)
    if user.game:
        keyboard = await game_keyboard(user)
        await message.answer(
            text=GAME_STARTED_MESSAGE, reply_markup=keyboard.as_markup()
        )
        return
    if not user.room:
        await message.answer(text=NOT_IN_ROOM_MESSAGE)
        return
    text = await get_players_in_room_message(user.room)
    if user.room.admin == user:
        keyboard = await inline_keyboards.room_admin_keyboard()
        await message.answer(
            text=text, reply_markup=keyboard.as_markup(), parse_mode="Markdown"
        )
        return
    await message.answer(text=text, parse_mode="Markdown")


@router.message(Command(commands.ENTER_GAME_ROOM_COMMAND))
@log_in_dev
async def enter_room_command(message: types.Message, state: FSMContext):
    """Хендлер перехода в состояние входа в комнату."""
    user = await get_user(message.from_user.id)
    if user.room:
        await message.answer(text=USER_CANT_ENTER_ROOM.format(user.room.slug))
        return
    await state.set_state(RoomState.enter_room_slug)
    keyboard = await cancel_state_keyboard()
    await message.answer(
        text=ENTER_ROOM_SLUG_MESSAGE, reply_markup=keyboard.as_markup()
    )


@router.message(Command(commands.LEAVE_GAME_ROOM_COMMAND))
@log_in_dev
async def leave_room_command(message: types.Message, state: FSMContext):
    """Хендлер выхода/закрытия комнаты в которой находится пользователь."""
    await state.clear()
    user = await get_user(message.from_user.id)
    room = user.room
    if room.admin == user:
        if room.started:
            user.game.is_closed = True
            await user.game.asave(update_fields=("is_closed",))
        async for player in User.objects.filter(room=room):
            player.game = None
            await player.asave(update_fields=("game",))
            await message.bot.send_message(
                chat_id=player.telegram_id,
                text=ROOM_IS_CLOSED_MESSAGE.format(get_user_url(user)),
                parse_mode="Markdown",
            )
        await room.adelete()
        return
    user.room = None
    user.game = None
    await user.asave(update_fields=("room", "game"))
    await message.answer(text=YOU_LEFT_ROOM_MESSAGE.format(room.slug))
    async for player in User.objects.filter(room=room):
        await message.bot.send_message(
            chat_id=player.telegram_id,
            text=PLAYER_LEFT_ROOM_MESSAGE.format(get_user_url(user)),
            parse_mode="Markdown",
        )
