from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.handlers.state import ChangeRobotComfig, ChangeGaz, ChangeCountGazWire
from bot.crud.crud import (
    add_updata_for_robot,
    get_user_by_id,
    add_updata_tip,
    add_updata_gaz,
    updata_gaz_ware
)
from main import logger

router = Router()


@router.message(F.text == 'Изменить комплектацию робота')
async def fork(message: Message) -> None:
    user = await get_user_by_id(message.from_user.id)
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='Замена наконечника'),
        KeyboardButton(text='Замена проволки'),
    )
    builder.row(
        KeyboardButton(text='Опеределить кол-во газа/Опеределить кол-во проволки'),
    )
    builder.row(
        KeyboardButton(text='Замена газа'),
    )
    builder.row(
        KeyboardButton(text=f'Робот {user.robot_id}'),
    )
    await message.answer(
        "Выбери что хочешь поменять",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@router.message(F.text == 'Замена проволки')
async def find_out_the_robot_equipment(
    message: Message,
    state: FSMContext
) -> None:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='Ultra'),
        KeyboardButton(text='08ХГСМФА'),
    )
    builder.row(
        KeyboardButton(text='12Х13'),
        KeyboardButton(text='06Х19Н9Т'),
    )
    builder.row(
        KeyboardButton(text='08Г2С'),
    )
    await message.answer(
        "На какую проволку меняешь?",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.set_state(ChangeRobotComfig.wire_mark)


@router.message(ChangeRobotComfig.wire_mark)
async def get_diametr(
    message: Message,
    state: FSMContext
) -> None:
    await state.update_data(wire_mark=message.text)
    await message.answer(
        "На какой диаметр?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='0.8'),
                    KeyboardButton(text='1.0'),
                    KeyboardButton(text='1.2'),
                    KeyboardButton(text='1.6'),
                ]
            ],
        ),
    )
    await state.set_state(ChangeRobotComfig.wire_diameter)


@router.message(ChangeRobotComfig.wire_diameter)
async def complite_change(
    message: Message,
    state: FSMContext
) -> None:
    await state.update_data(wire_diameter=message.text)
    data = await state.get_data()
    diameter = data.get('wire_diameter')
    mark = data.get('wire_mark')
    user = await get_user_by_id(message.from_user.id)
    await add_updata_for_robot(
        diametr=diameter,
        mark=mark,
        last_updata_men=user.name,
        robot=user.robot_id,
        last_updata_men_sur=user.surname,
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
    await state.clear()


@router.message(F.text == 'Замена наконечника')
async def tip_change(
    message: Message,
) -> None:
    user = await get_user_by_id(message.from_user.id)
    await add_updata_tip(
        last_updata_men=user.name,
        robot_id=user.robot_id,
        last_updata_men_sur=user.surname
    )
    updated_user = await get_user_by_id(message.from_user.id)
    logger.info(f"User after tip change: {updated_user}")
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


@router.message(F.text == 'Замена газа')
async def gaz_change(
    message: Message,
    state: FSMContext
) -> None:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='Ar 100%'),
        KeyboardButton(text='Ar-98% CO2-2%'),
    )
    builder.row(
        KeyboardButton(text='Ar-80% CO2-20%'),
    )
    builder.row(
        KeyboardButton(text='CO2 100%'),
        KeyboardButton(text='He 100%'),
    )
    await message.answer(
        "На что меняешь?",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.set_state(ChangeGaz.gaz_name)


@router.message(ChangeGaz.gaz_name)
async def gaz_change_state(
    message: Message,
    state: FSMContext
) -> None:
    user = await get_user_by_id(message.from_user.id)
    await add_updata_gaz(
        robot=user.robot_id,
        last_updata_men=user.name,
        gaz_name=message.text,
        last_updata_men_sur=user.surname
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
    await state.clear()


@router.message(F.text == 'Опеределить кол-во газа/Опеределить кол-во проволки')
async def get_gaz_ware(
    message: Message,
    state: FSMContext
) -> None:
    await message.answer(
        "Сколько осталось проволки? (Ввести число от 1 до 10)",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(ChangeCountGazWire.ware_count)


@router.message(ChangeCountGazWire.ware_count)
async def get_gaz_ware_state(
    message: Message,
    state: FSMContext
) -> None:
    if not message.text.isdigit() or not 1 <= int(message.text) <= 10:
        await message.answer(
            'Ввести число от 1 до 10, без дробной части'
        )
        return
    else:
        await state.update_data(ware_count=int(message.text))
        await message.answer(
            "Сколько осталось газа? (Ввести число в AТМ)",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(ChangeCountGazWire.gaz_count)


@router.message(ChangeCountGazWire.gaz_count)
async def get_gaz_ware_state_end(
    message: Message,
    state: FSMContext
) -> None:
    if ',' in message.text:
        await message.answer(
            'Нужно использовать точку'
        )
        return
    elif float(message.text) < 0:
        await message.answer(
            'Газ не может быть меньше 0'
        )
        return
    else:
        await state.update_data(gaz_count=float(message.text))
        data = await state.get_data()
        ware_count = data.get('ware_count')
        gaz_count = data.get('gaz_count')
        user = await get_user_by_id(message.from_user.id)
        await updata_gaz_ware(
            robot=user.robot_id,
            last_updata_men=user.name,
            ware_count=ware_count,
            gaz_count=gaz_count,
            last_updata_men_sur=user.surname
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
        await state.clear()
