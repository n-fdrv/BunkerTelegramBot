from typing import Optional

from aiogram.filters.callback_data import CallbackData


class BaseCallbackData(CallbackData, prefix="pac"):
    """Базовый Callback_data."""

    action: str
    id: Optional[int] = None
    page: int = 1
    back_action: Optional[str] = None


class RoomCallbackData(BaseCallbackData, prefix="r"):
    """Callback_data для комнат."""

    player_id: Optional[int] = None


class GameCallbackData(BaseCallbackData, prefix="g"):
    """Callback_data для игры."""

    pass


CALLBACK_DATA_PREFIX = {
    RoomCallbackData.__prefix__: RoomCallbackData,
    GameCallbackData.__prefix__: GameCallbackData,
}
