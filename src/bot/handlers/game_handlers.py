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
    if not started:
        await callback.message.answer(text=text)
        return
    keyboard = await game_keyboard(callback_data=callback_data)
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
    keyboard = await game_keyboard(callback_data=callback_data)
    character = await Character.objects.select_related(
        "profession",
        "gender",
        "orientation",
        "health",
        "phobia",
        "hobby",
        "personality",
        "information",
        "item",
        "action_one",
        "action_two",
    ).aget(user=user, game__is_closed=False)
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
    user = await User.objects.select_related("game__epidemia").aget(
        telegram_id=callback.from_user.id
    )
    keyboard = await game_keyboard(callback_data=callback_data)
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
    ).aget(telegram_id=callback.from_user.id)
    keyboard = await game_keyboard(callback_data=callback_data)
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
