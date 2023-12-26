from bot.constants.callback_data import CALLBACK_DATA_PREFIX


def get_callback_by_action(action):
    """Получения CallbackFactory из callback_data.action."""
    data = action.split("-")
    return CALLBACK_DATA_PREFIX[data[0]](action=action)
