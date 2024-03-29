from aiogram import Router, types
from aiogram.filters import KICKED, ChatMemberUpdatedFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatMemberUpdated
from game.models import TypeInformationCarts
from game.utils.room import get_players_in_room_message

from bot.constants import commands
from bot.constants.messages import (
    EPIDEMIA_GET_MESSAGE,
    HELP_MESSAGE,
    START_MESSAGE,
    SUPPORT_MESSAGE,
)
from bot.keyboards.inline_keyboards import (
    game_keyboard,
    room_keyboard,
    start_keyboard,
    support_keyboard,
)
from bot.models import User
from bot.utils.user_helpers import get_user
from core.config.logging import log_in_dev

router = Router()


@router.message(Command(commands.START_COMMAND))
@log_in_dev
async def start_handler(message: types.Message, state: FSMContext):
    """Хендлер при нажатии кнопки start."""
    await state.clear()
    user, created = await User.objects.select_related(
        "room", "game", "room__admin"
    ).aget_or_create(
        telegram_id=message.from_user.id,
    )
    if not created:
        user.is_active = True
        await user.asave(update_fields=("is_active",))
    user.first_name = message.from_user.first_name
    user.last_name = message.from_user.last_name
    user.telegram_username = message.from_user.username
    keyboard = await start_keyboard()
    await user.asave(
        update_fields=("first_name", "last_name", "telegram_username")
    )
    if user.game:
        keyboard = await game_keyboard(user)
        await message.answer(
            text=EPIDEMIA_GET_MESSAGE.format(
                await user.game.information_carts.filter(
                    type=TypeInformationCarts.EPIDEMIA
                ).alast(),
                user.game.epidemia_time,
            ),
            reply_markup=keyboard.as_markup(),
        )
        return

    if user.room:
        text = await get_players_in_room_message(user.room)
        keyboard = await room_keyboard(user)
        await message.answer(
            text=text, reply_markup=keyboard.as_markup(), parse_mode="Markdown"
        )
        return

    await message.answer(text=START_MESSAGE, reply_markup=keyboard.as_markup())


@router.message(Command(commands.HELP_COMMAND))
@log_in_dev
async def help_handler(message: types.Message, state: FSMContext):
    """Хендлер команды help."""
    await message.answer(text=HELP_MESSAGE)


@router.message(Command(commands.SUPPORT_COMMAND))
@log_in_dev
async def support_handler(message: types.Message, state: FSMContext):
    """Хендлер команды rules."""
    keyboard = await support_keyboard()
    await message.answer(
        text=SUPPORT_MESSAGE, reply_markup=keyboard.as_markup()
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
@log_in_dev
async def block_handler(event: ChatMemberUpdated, state: FSMContext):
    """Хендлер при блокировке бота."""
    await state.clear()
    user = await get_user(event.from_user.id)
    user.is_active = False
    await user.asave(update_fields=("is_active",))
