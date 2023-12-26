class Action:
    """Базовый класс действий для callback_data."""

    get = "get"
    create = "create"
    remove = "remove"
    list = "list"
    update = "update"

    def __init__(self, callback_name):
        """Добавляет префикс ко всем основным действиям."""
        self.callback = f"{callback_name}-"
        self.get = self.callback + self.get
        self.create = self.callback + self.create
        self.remove = self.callback + self.remove
        self.list = self.callback + self.list
        self.update = self.callback + self.update

    def __str__(self):
        return self.callback


class RoomAction(Action):
    """Действия для callback_data комнат."""

    enter = "r-e"
    rules = "r-r"
    cancel = "r-c"
    begin = "r-b"
    players = "r=p"
    close_room = "r-cr"
    player_get = "r-pg"
    player_kick = "r=kp"
    admin_get = "r-ag"


room_action = RoomAction("r")
