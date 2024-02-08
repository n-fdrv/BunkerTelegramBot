from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.conf import settings
from game.models import Room

from bot.constants import buttons, messages
from bot.constants.actions import (
    action_cart_action,
    game_action,
    room_action,
    start_action,
)
from bot.constants.callback_data import (
    ActionCartCallbackData,
    GameCallbackData,
    RoomCallbackData,
    StartCallbackData,
)
from bot.models import User
from bot.utils.back_button_builder import back_builder


async def start_keyboard():
    """Клавиатура при команде /start."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=buttons.CREATE_ROOM_BUTTON,
        callback_data=RoomCallbackData(action=room_action.create),
    )
    keyboard.button(
        text=buttons.ENTER_ROOM_BUTTON,
        callback_data=RoomCallbackData(action=room_action.enter),
    )
    keyboard.button(
        text=buttons.ABOUT_BUTTON,
        callback_data=StartCallbackData(action=start_action.about),
    )
    keyboard.button(
        text=buttons.RULES_BUTTON,
        callback_data=StartCallbackData(action=start_action.rules),
    )
    keyboard.button(
        text=buttons.HELP_BUTTON,
        callback_data=StartCallbackData(action=start_action.help),
    )
    keyboard.adjust(1)
    return keyboard


async def support_keyboard():
    """Клавиатура поддержки."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=buttons.SUPPORT_BUTTON, url=settings.SUPPORT_FORM_URL)
    keyboard.adjust(1)
    return keyboard


async def help_keyboard():
    """Клавиатура помощи."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=buttons.BACK_BUTTON,
        callback_data=StartCallbackData(action=start_action.get),
    )
    keyboard.adjust(1)
    return keyboard


async def about_keyboard(page: int = 1):
    """Клавиатура об игре."""
    keyboard = InlineKeyboardBuilder()
    if page == 1:
        keyboard.button(
            text=buttons.NEXT_PAGE_BUTTON,
            callback_data=StartCallbackData(
                action=start_action.about, page=page + 1
            ),
        )
    else:
        keyboard.button(
            text=buttons.PREVIOUS_PAGE_BUTTON,
            callback_data=StartCallbackData(
                action=start_action.about, page=page - 1
            ),
        )
    keyboard.button(
        text=buttons.BACK_BUTTON,
        callback_data=StartCallbackData(action=start_action.get),
    )
    keyboard.adjust(1)
    return keyboard


async def rules_keyboard(page: int = 1):
    """Клавиатура правил игры."""
    keyboard = InlineKeyboardBuilder()
    buttons_number = 0
    page_amount = len(messages.RULES_MESSAGE)
    if page > 1:
        keyboard.button(
            text=buttons.PREVIOUS_PAGE_BUTTON,
            callback_data=StartCallbackData(
                action=start_action.rules, page=page - 1
            ),
        )
        buttons_number += 1
    if page < page_amount:
        keyboard.button(
            text=buttons.NEXT_PAGE_BUTTON,
            callback_data=StartCallbackData(
                action=start_action.rules, page=page + 1
            ),
        )
        buttons_number += 1
    keyboard.button(
        text=buttons.BACK_BUTTON,
        callback_data=StartCallbackData(action=start_action.get),
    )
    keyboard.adjust(buttons_number, 1)
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


async def room_keyboard(user):
    """Метод формирования клавиатуры комнаты."""
    keyboard = InlineKeyboardBuilder()
    exit_button = buttons.EXIT_ROOM_BUTTON
    if user == user.room.admin:
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
        exit_button = buttons.CLOSE_ROOM_BUTTON
    keyboard.button(
        text=exit_button,
        callback_data=RoomCallbackData(action=room_action.exit_room),
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
    keyboard = await back_builder(keyboard, room_action.get)
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
    keyboard.button(
        text=buttons.ALL_INFO_BUTTON,
        callback_data=GameCallbackData(
            action=game_action.get_all_info, id=user.game.pk
        ),
    )
    keyboard.button(
        text=buttons.ACTION_LIST_BUTTON,
        callback_data=ActionCartCallbackData(action=action_cart_action.list),
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


async def game_all_info_keyboard(
    user: User, callback_data: GameCallbackData = None
):
    """Клавиатура режима игры в одном сообщении."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=buttons.EXIT_ALL_INFO_BUTTON,
        callback_data=GameCallbackData(
            action=game_action.get_epidemia, id=user.game.pk
        ),
    )
    keyboard.button(
        text=buttons.ACTION_LIST_BUTTON,
        callback_data=ActionCartCallbackData(action=action_cart_action.list),
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
