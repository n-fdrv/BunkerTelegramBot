from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.constants import messages
from bot.constants.actions import game_action
from bot.constants.callback_data import GameCallbackData
from bot.constants.messages import CHARACTER_GET_MESSAGE
from bot.keyboards.inline_keyboards import game_keyboard
from bot.models import Character, User
from bot.utils.game_helpers import start_game
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
    user = await User.objects.select_related("room").aget(
        telegram_id=callback.from_user.id
    )
    text, started = await start_game(user.room)
    await callback.message.answer(text=text)
    if not started:
        return
    keyboard = await game_keyboard()
    async for player in User.objects.filter(room=user.room).all():
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
    user = await User.objects.select_related("room", "room__admin").aget(
        telegram_id=callback.from_user.id
    )
    character = await Character.objects.aget(user=user, room=user.room)
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
