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


class StartAction(Action):
    """Действия для callback_data старта."""

    about = "st-about"
    help = "st-help"
    rules = "st-rules"


class RoomAction(Action):
    """Действия для callback_data комнат."""

    create = "r-cr"
    enter = "r-en"
    cancel = "r-c"
    players = "r-p"
    exit_room = "r-exr"
    player_get = "r-pg"
    player_kick = "r-kp"


class GameAction(Action):
    """Действия для callback_data игр."""

    start = "g-s"
    get_epidemia = "g-ge"
    get_bunker = "g-gb"
    get_character = "g-gc"
    get_all_info = "g-gai"
    game_settings = "g-gs"
    reload_game = "g-rg"
    close_game = "g-cg"


class ActionCartAction(Action):
    """Действия для callback_data действий."""

    use_cart = "ac-us"
    choose_target = "ac-ct"


room_action = RoomAction("r")
game_action = GameAction("g")
start_action = StartAction("st")
action_cart_action = ActionCartAction("ac")
