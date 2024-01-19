from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.constants import buttons
from bot.constants.actions import game_action, room_action
from bot.constants.callback_data import GameCallbackData, RoomCallbackData
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
        callback_data=GameCallbackData(action=game_action.start),
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
    """Метод формирования клавиатуры просмотра игроков в лобби."""
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


async def game_keyboard(user: User, callback_data: GameCallbackData = None):
    """Метод получения клавиатуры управления игрой."""
    keyboard = InlineKeyboardBuilder()
    action = None
    if callback_data:
        action = callback_data.action
    if action != game_action.get_epidemia:
        keyboard.button(
            text=buttons.EPIDEMIA_BUTTON,
            callback_data=GameCallbackData(
                action=game_action.get_epidemia, id=user.game.pk
            ),
        )
    if action != game_action.get_bunker:
        keyboard.button(
            text=buttons.BUNKER_BUTTON,
            callback_data=GameCallbackData(
                action=game_action.get_bunker, id=user.game.pk
            ),
        )
    if action != game_action.get_character:
        keyboard.button(
            text=buttons.CHARACTER_BUTTON,
            callback_data=GameCallbackData(
                action=game_action.get_character, id=user.game.pk
            ),
        )
    if user.room.admin == user:
        keyboard.button(
            text=buttons.ROOM_SETTINGS_BUTTON,
            callback_data=GameCallbackData(
                action=game_action.game_settings, id=user.game.pk
            ),
        )
    keyboard.adjust(1)
    return keyboard


async def game_settings_keyboard():
    """Метод формирования клавиатуры настроек игры."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=buttons.RELOAD_GAME_BUTTON,
        callback_data=GameCallbackData(action=game_action.reload_game),
    )
    keyboard.button(
        text=buttons.CLOSE_GAME_BUTTON,
        callback_data=GameCallbackData(action=game_action.close_game),
    )
    keyboard = await back_builder(keyboard, game_action.get_epidemia)
    keyboard.adjust(1)
    return keyboard
