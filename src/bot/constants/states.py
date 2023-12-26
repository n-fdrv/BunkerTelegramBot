from aiogram.fsm.state import State, StatesGroup


class RoomState(StatesGroup):
    """Состояние при вводе slug комнаты."""

    enter_room_slug = State()
