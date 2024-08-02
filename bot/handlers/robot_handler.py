from aiogoogle import Aiogoogle

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from fastapi import Depends

from bot.crud.crud import (
    add_robot_for_operator,
    get_cell_number,
    get_current_robot_statistic, get_user_by_id
)

router = Router()


@router.message(F.text == 'Робот 1')
@router.message(F.text == 'Робот 2')
async def take_robot(
    message: Message,
    state: FSMContext
) -> None:
    await state.clear()
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='Состояние установки'),
    )
    builder.row(
        KeyboardButton(text='Обслуживание установки'),
    )
    builder.row(
        KeyboardButton(text='Регистация дефектов'),
    )
    builder.row(
        KeyboardButton(text='Наблюдения'),
    )
    builder.row(
        KeyboardButton(text='Завершить сессию на роботе'),
    )
    if message.text == 'Робот 1':
        robot_id_in_funk = 1
    elif 'Робот 2':
        robot_id_in_funk = 2
    await add_robot_for_operator(
        telegramm_id=message.from_user.id,
        robot=robot_id_in_funk
    )
    await message.answer(
        'Молодец, приступай к работе ',
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@router.message(F.text == 'Состояние установки')
async def find_out_the_robot_equipment_t(
    message: Message
) -> None:
    user = await get_user_by_id(message.from_user.id)
    cell_number = await get_cell_number(message.from_user.id)
    curent_robot_state = await get_current_robot_statistic(cell_number)
    tip_updata = curent_robot_state.tip_data_change.strftime('%H:%M')
    await message.answer(
        f'Сводная информация по {cell_number}',
    )
    await message.answer(
        f'Проволки осталось - {curent_robot_state.wire}/10\n'
        f'Проволка - {curent_robot_state.wire_mark}\n'
        f'Диаметр - {curent_robot_state.wire_diameter}\n'
        f'Прошлая смена наконечника - {tip_updata}\n'
        f'Газ {curent_robot_state.name_gaz} - {curent_robot_state.gaz_state} АТМ\n'
        f'Произвел - {curent_robot_state.last_updata_men} {curent_robot_state.last_updata_men_sur}\n',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=f'Робот {user.robot_id}'),
                ]
            ],
        ),
    )
