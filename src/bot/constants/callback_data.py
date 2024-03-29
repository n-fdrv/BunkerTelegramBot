from typing import Optional

from aiogram.filters.callback_data import CallbackData


class BaseCallbackData(CallbackData, prefix="pac"):
    """Базовый Callback_data."""

    action: str
    id: Optional[int] = None
    page: int = 1
    back_action: Optional[str] = None


class StartCallbackData(BaseCallbackData, prefix="st"):
    """Callback_data для игры."""

    pass


class RoomCallbackData(BaseCallbackData, prefix="r"):
    """Callback_data для комнат."""

    player_id: Optional[int] = None


class GameCallbackData(BaseCallbackData, prefix="g"):
    """Callback_data для игры."""

    pass


class ActionCartCallbackData(BaseCallbackData, prefix="ac"):
    """Callback_data для действий."""

    target: Optional[int] = None


CALLBACK_DATA_PREFIX = {
    RoomCallbackData.__prefix__: RoomCallbackData,
    GameCallbackData.__prefix__: GameCallbackData,
    StartCallbackData.__prefix__: StartCallbackData,
    ActionCartCallbackData.__prefix__: ActionCartCallbackData,
}
