from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardRemove

from bot.crud.add_robot import create_robot
from bot.handlers.state import UserState
from bot.crud.crud_for_add import get_user_by_id, create_user, get_current_robot_statistic


router = Router()


@router.message(F.text == 'Завершить сессию на роботе')
@router.message(F.text == 'В стартовое меню')
@router.message(CommandStart())
async def command_start(
    message: Message,
) -> None:
    if await get_user_by_id(message.from_user.id) == None:
        await message.answer(
            'Привет заводчанин, как сменка?\n'
            'Жаль что я бездушный скрипт и ничего не могу ответить',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text='Узнать состояние роботов'),
                        KeyboardButton(text='Зарегаться (временная кнопка)'),
                    ]
                ],
            ),
        )
    else:
        await message.answer(
            'Привет заводчанин, как сменка?\n'
            'Жаль что я бездушный скрипт и ничего не могу ответить',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text='Занять робота'),
                        KeyboardButton(text='Узнать состояние роботов'),
                    ]
                ],
            ),
        )


@router.message(F.text == 'Занять робота')
async def take_robot(
    message: Message
) -> None:
    await message.answer(
        'Где сегодня будешь работать?\n "На работе" не считаеться',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Робот 1'),
                    KeyboardButton(text='Робот 2'),
                ]
            ],
        ),
    )


@router.message(F.text == 'Зарегаться (временная кнопка)')
async def create_user_state_first(
    message: Message,
    state: FSMContext
) -> None:
    await state.set_state(UserState.name)
    await message.answer(
        "Кто ты? (Желательно имя и Фамилия)",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(UserState.name)
async def create_user_state_second(
    message: Message,
    state: FSMContext
) -> None:
    name, surname = message.text.split()
    if name.isalpha():
        await message.answer(
            f"Поверю что {name} {surname} - ты",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text='В стартовое меню'),
                    ]
                ],
            ),
        )
        await create_user(
            telegramm_id=message.from_user.id,
            name=name,
            surname=surname
        )
        await state.clear()
    else:
        await message.answer(
            "Я понимаю что ввести свое имя - трудно очень, но попробуй еще раз",
            reply_markup=ReplyKeyboardRemove(),
        )
        await create_user_state_second()


@router.message(F.text == 'Добавить робота')
async def add_ro(message: Message):
    await create_robot()
    await message.answer(
        f"Проверяй",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='В стартовое меню'),
                ]
            ],
        ),
    )


@router.message(F.text == 'Узнать состояние роботов')
async def add_ro(message: Message):
    curent_robot_state = await get_current_robot_statistic(1)
    curent_robot_state_t = await get_current_robot_statistic(2)
    tip_updata = curent_robot_state.tip_data_change.strftime('%H:%M')
    tip_updata_t = curent_robot_state_t.tip_data_change.strftime('%H:%M')
    await message.answer(
        'Робот 1\n'
        f'Проволки осталось - {curent_robot_state.wire}/10\n'
        f'Проволка - {curent_robot_state.wire_mark}\n'
        f'Диаметр - {curent_robot_state.wire_diameter}\n'
        f'Прошлая смена наконечника - {tip_updata}\n'
        f'Газ {curent_robot_state.name_gaz} - {curent_robot_state.gaz_state} АТМ\n'
        f'Произвел - {curent_robot_state.last_updata_men} {curent_robot_state.last_updata_men_sur}\n',
    )
    await message.answer(
        'Робот 2\n'
        f'Проволки осталось - {curent_robot_state_t.wire}/10\n'
        f'Проволка - {curent_robot_state_t.wire_mark}\n'
        f'Диаметр - {curent_robot_state_t.wire_diameter}\n'
        f'Прошлая смена наконечника - {tip_updata_t}\n'
        f'Газ {curent_robot_state.name_gaz} - {curent_robot_state.gaz_state} АТМ\n'
        f'Произвел - {curent_robot_state_t.last_updata_men} {curent_robot_state.last_updata_men_sur}\n',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='В стартовое меню'),
                ]
            ],
        ),
    )
