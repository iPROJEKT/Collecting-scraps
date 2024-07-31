from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardRemove

from bot.crud.crud_for_add import get_user_by_id, save_observations
from bot.handlers.state import ObserverState

router = Router()


@router.message(F.text == 'Наблюдения')
async def observations_handler(
    message: Message,
    state: FSMContext
) -> None:
    await state.set_state(ObserverState.message)
    await message.answer(
        "Чем хочешь поделиться?",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(ObserverState.message)
async def observer_stete(message: Message, state: FSMContext) -> None:
    user = await get_user_by_id(message.from_user.id)
    await state.update_data(message=message.text)
    await save_observations(
        user_id=user.user_id,
        id_robot=user.robot_id,
        comment=message.text
    )
    await message.answer(
        "Успешно",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=f'Робот {user.robot_id}'),
                ]
            ],
        ),
    )
