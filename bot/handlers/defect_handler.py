from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.handlers.state import DefectState
from bot.crud.crud import create_defect, get_cell_number, get_user_by_id

router = Router()


@router.message(F.text == 'Регистация дефектов')
async def defect_start_handler(
    message: Message,
    state: FSMContext
) -> None:
    user = await get_user_by_id(message.from_user.id)
    print(message.from_user.id)
    builder = ReplyKeyboardBuilder()
    await state.set_state(DefectState.name_of_defect)
    builder.row(
        KeyboardButton(text="Поры"),
        KeyboardButton(text="Трещины")
    )
    builder.row(
        KeyboardButton(text='Несплавления'),
        KeyboardButton(text='Выплески/ брызги металла'),
    )
    builder.row(
        KeyboardButton(text='Деформации'),
        KeyboardButton(text='Подрезы'),
        KeyboardButton(text='Прожиги'),
    )
    builder.row(
        KeyboardButton(text=f'Робот {user.robot_id}'),
    )
    await message.answer(
        'Выбери дефект',
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@router.message(DefectState.name_of_defect)
async def defect_name_of_defect(
    message: Message,
    state: FSMContext
) -> None:
    print(message.from_user.id)
    await state.update_data(name_of_defect=message.text)
    await state.set_state(DefectState.what_happened)
    await message.answer(
        'Чего наблюдаем?',
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(DefectState.what_happened)
async def defect_name_main_program(
    message: Message,
    state: FSMContext
) -> None:
    print(message.from_user.id)
    await state.update_data(what_happened=message.text)
    await state.set_state(DefectState.name_mp)
    await message.answer(
        'Имя главной программы',
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(DefectState.name_mp)
async def defect_defect_coordinates(
    message: Message,
    state: FSMContext
) -> None:
    print(message.from_user.id)
    await state.update_data(name_mp=message.text)
    await state.set_state(DefectState.defect_coordinates)
    await message.answer(
        'Координаты дефекта(ов) в активном фрейме (X,Y,Z)',
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(DefectState.defect_coordinates)
async def defect_end_state(
    message: Message,
    state: FSMContext
) -> None:
    await state.update_data(defect_coordinates=message.text)
    user = await get_user_by_id(message.from_user.id)
    data = await state.get_data()
    name_of_defect = data.get('name_of_defect')
    what_happened = data.get('what_happened')
    name_mp = data.get('name_mp')
    defect_coordinates = data.get('defect_coordinates')
    robot_id = await get_cell_number(message.from_user.id)

    await create_defect(
        robot=robot_id,
        name_of_defect=name_of_defect,
        what_happened=what_happened,
        name_mp=name_mp,
        defect_coordinates=defect_coordinates,
        name_user=user
    )
    await message.answer(
        "Кто ничего не делает - тот не ошибается. Но постарайся без брака",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=f'Робот {user.robot_id}'),
                ]
            ],
        ),
    )
    await state.clear()
