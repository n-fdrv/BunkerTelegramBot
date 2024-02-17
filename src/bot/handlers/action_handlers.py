from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from game.models import ActionCart, ActionCharacter, Character, TargetAction
from game.utils.cart import check_is_used_cart, use_action_cart
from game.utils.character import get_character, get_character_info_text

from bot.constants import messages
from bot.constants.actions import action_cart_action
from bot.constants.callback_data import ActionCartCallbackData
from bot.constants.messages_data import action_messages
from bot.keyboards import action_keyboards
from bot.keyboards.inline_keyboards import game_keyboard
from bot.utils.user_helpers import get_user, get_user_url
from core.config.logging import log_in_dev

router = Router()


@router.callback_query(
    ActionCartCallbackData.filter(F.action == action_cart_action.list)
)
@log_in_dev
async def action_list(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: ActionCartCallbackData,
):
    """Хендлер списка карт."""
    user = await get_user(callback.from_user.id)
    if not user.game:
        await callback.message.edit_text(text=messages.NO_GAME_MESSAGE)
        return
    character = await get_character(user)
    keyboard = await action_keyboards.action_list_keyboard(character)
    await callback.message.edit_text(
        text=action_messages.LIST_MESSAGE, reply_markup=keyboard.as_markup()
    )


@router.callback_query(
    ActionCartCallbackData.filter(F.action == action_cart_action.get)
)
@log_in_dev
async def action_get(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: ActionCartCallbackData,
):
    """Хендлер получения определенной карты."""
    user = await get_user(callback.from_user.id)
    if not user.game:
        await callback.message.edit_text(text=messages.NO_GAME_MESSAGE)
        return
    character = await get_character(user)
    cart = await ActionCart.objects.aget(pk=callback_data.id)
    if not cart.is_active or await check_is_used_cart(character, cart):
        keyboard = await action_keyboards.not_active_cart_keyboard()
        await callback.message.edit_text(
            text=action_messages.NOT_ACTIVE_CART,
            reply_markup=keyboard.as_markup(),
        )
        return
    if cart.target == TargetAction.ANY:
        keyboard = await action_keyboards.choose_target_keyboard(
            callback_data, user.game
        )
        await callback.message.edit_text(
            text=action_messages.CHOOSE_TARGET_MESSAGE,
            reply_markup=keyboard.as_markup(),
        )
        return
    await state.update_data(target=[character])
    if cart.target == TargetAction.ALL:
        target_data = []
        async for target in (
            Character.objects.select_related("game")
            .filter(game=user.game)
            .aall()
        ):
            target_data.append(target)
        await state.update_data(target=target_data)
    keyboard = await action_keyboards.cart_confirmation_keyboard(callback_data)
    await callback.message.edit_text(
        text=action_messages.CONFIRMATION_MESSAGE,
        reply_markup=keyboard.as_markup(),
    )


@router.callback_query(
    ActionCartCallbackData.filter(F.action == action_cart_action.choose_target)
)
@log_in_dev
async def choose_target(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: ActionCartCallbackData,
):
    """Хендлер подверждения выбранной цели."""
    user = await get_user(callback.from_user.id)
    if not user.game:
        await callback.message.edit_text(text=messages.NO_GAME_MESSAGE)
        return
    target = await get_user(callback_data.target)
    await state.update_data(target=[await get_character(target)])
    keyboard = await action_keyboards.cart_confirmation_keyboard(callback_data)
    await callback.message.edit_text(
        text=action_messages.CONFIRMATION_MESSAGE,
        reply_markup=keyboard.as_markup(),
    )


@router.callback_query(
    ActionCartCallbackData.filter(F.action == action_cart_action.use_cart)
)
@log_in_dev
async def use_cart(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: ActionCartCallbackData,
):
    """Хендлер использования карты."""
    user = await get_user(callback.from_user.id)
    if not user.game:
        await callback.message.edit_text(text=messages.NO_GAME_MESSAGE)
        return
    cart = await ActionCart.objects.aget(pk=callback_data.id)
    data = await state.get_data()
    character = await get_character(user)
    character_action = (
        await ActionCharacter.objects.select_related(
            "cart", "character", "character__game"
        )
        .filter(cart=cart, character=character)
        .alast()
    )
    await use_action_cart(character_action, data["target"])
    keyboard = await game_keyboard(user)
    character = await get_character(user)
    await callback.message.edit_text(
        text=await get_character_info_text(character),
        reply_markup=keyboard.as_markup(),
    )
    async for player in user.game.users.all():
        await callback.message.bot.send_message(
            chat_id=player.telegram_id,
            text=action_messages.SUCCESS_USING_CART.format(
                get_user_url(user), cart.name
            ),
            parse_mode="Markdown",
        )
