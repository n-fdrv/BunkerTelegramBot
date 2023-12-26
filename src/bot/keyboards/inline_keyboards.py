from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.constants import buttons
from bot.constants.actions import room_action
from bot.constants.callback_data import RoomCallbackData
from bot.models import Room, User
from bot.utils.back_button_builder import back_builder


async def cancel_state_keyboard():
    """Метод формирования выхода из комнаты/отмены состояния входа."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=buttons.CANCEL_BUTTON,
        callback_data=RoomCallbackData(action=room_action.cancel),
    )
    keyboard.adjust(1)
    return keyboard


async def room_admin_keyboard():
    """Метод формирования клавиатуры администратора комнаты."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=buttons.BEGIN_BUTTON,
        callback_data=RoomCallbackData(action=room_action.begin),
    )
    keyboard.button(
        text=buttons.DISMISS_PLAYERS_BUTTON,
        callback_data=RoomCallbackData(
            action=room_action.players,
        ),
    )
    keyboard.adjust(1)
    return keyboard


async def show_players_keyboard(room: Room):
    """Метод формирования клавиатуры администратора комнаты."""
    keyboard = InlineKeyboardBuilder()
    rows = []
    async for player in User.objects.filter(room=room).all():
        keyboard.button(
            text=f"{player.first_name} {player.last_name}",
            callback_data=RoomCallbackData(
                action=room_action.player_get, player_id=player.telegram_id
            ),
        )
        btn_text = buttons.DISMISS_BUTTON
        btn_action = room_action.player_kick
        if room.admin == player:
            btn_text = "Администратор"
            btn_action = room_action.player_get
        keyboard.button(
            text=btn_text,
            callback_data=RoomCallbackData(
                action=btn_action, player_id=player.telegram_id
            ),
        )
        rows.append(2)
    keyboard = await back_builder(keyboard, room_action.admin_get)
    keyboard.adjust(*rows, 1)
    return keyboard
