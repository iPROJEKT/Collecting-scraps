from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    name = State()


class ChangeRobotComfig(StatesGroup):
    wire_mark = State()
    wire_diameter = State()


class ChangeGaz(StatesGroup):
    gaz_name = State()


class ChangeCountGazWire(StatesGroup):
    gaz_count = State()
    ware_count = State()


class DefectState(StatesGroup):
    name_of_defect = State()
    what_happened = State()
    name_mp = State()
    defect_coordinates = State()


class ObserverState(StatesGroup):
    message = State()
