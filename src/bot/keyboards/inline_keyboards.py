from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.constants import buttons
from bot.constants.actions import room_action
from bot.constants.callback_data import RoomCallbackData
from bot.models import Room, User
from bot.utils.back_button_builder import back_builder


async def start_keyboard():
    """Метод формирования основной клавиатуры."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=buttons.ENTER_ROOM_BUTTON,
        callback_data=RoomCallbackData(action=room_action.enter),
    )
    keyboard.button(
        text=buttons.CREATE_ROOM_BUTTON,
        callback_data=RoomCallbackData(action=room_action.create),
    )
    keyboard.button(
        text=buttons.RULES_BUTTON,
        callback_data=RoomCallbackData(action=room_action.rules),
    )
    keyboard.adjust(1)
    return keyboard


async def cancel_state_keyboard():
    """Метод формирования выхода из комнаты/отмены состояния входа."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=buttons.CANCEL_BUTTON,
        callback_data=RoomCallbackData(action=room_action.cancel),
    )
    keyboard.adjust(1)
    return keyboard


async def room_admin_keyboard(room: Room):
    """Метод формирования клавиатуры администратора комнаты."""
    keyboard = InlineKeyboardBuilder()
    players_amount = await User.objects.filter(room=room).acount()
    keyboard.button(
        text=buttons.BEGIN_BUTTON,
        callback_data=RoomCallbackData(action=room_action.begin),
    )
    keyboard.button(
        text=buttons.PLAYERS_BUTTON.format(players_amount),
        callback_data=RoomCallbackData(
            action=room_action.players,
        ),
    )
    keyboard.button(
        text=buttons.CLOSE_ROOM_BUTTON,
        callback_data=RoomCallbackData(action=room_action.close_room),
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
            callback_data=RoomCallbackData(action=room_action.player_get),
        )
        btn_text = buttons.DISMISS_PLAYER
        if room.admin == player:
            btn_text = "Администратор"
        keyboard.button(
            text=btn_text,
            callback_data=RoomCallbackData(
                action=room_action.player_kick,
            ),
        )
        rows.append(2)
    keyboard = await back_builder(keyboard, room_action.admin_get)
    keyboard.adjust(*rows, 1)
    return keyboard
