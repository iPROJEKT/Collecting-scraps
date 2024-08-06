import pytz

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float

from bot.core.utils import moscow_now
from bot.models.base import Base


MOSCOW_TZ = pytz.timezone('Europe/Moscow')


class LilWAAMerNigga(Base):
    """Называю калассы как хочу, если кто увидит - круто будет"""
    user_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, unique=False, nullable=False)
    surname = Column(String, unique=False, nullable=True)
    robot_id = Column(Integer, default=0)


class Incident(Base):
    """Тут фантазия кончилась"""
    number_robot = Column(Integer, unique=False, nullable=False)
    incident = Column(String, unique=False, nullable=False)
    datatime = Column(DateTime, default=moscow_now(MOSCOW_TZ))
    comment = Column(String, unique=False, nullable=False)
    name_main_programm = Column(String, unique=False, nullable=True)
    coord = Column(String, unique=False, nullable=True)
    name_user = Column(String, unique=False, nullable=True)


class RobotState(Base):
    """Состояние робота на данный момент"""
    id_robot = Column(Integer, nullable=False)
    wire = Column(Integer, nullable=False)
    wire_mark = Column(String, nullable=False)
    wire_diameter = Column(Float, nullable=False)
    gaz_state = Column(Float, nullable=True, default=5.0)
    name_gaz = Column(String, nullable=True)
    tip_data_change = Column(DateTime, default=moscow_now(MOSCOW_TZ))
    datatime = Column(DateTime, default=moscow_now(MOSCOW_TZ))
    last_updata_men = Column(String, nullable=True)
    last_updata_men_sur = Column(String, nullable=True)
    busy = Column(Boolean, nullable=False)


class Observations(Base):
    id_robot = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False, unique=False)
    comment = Column(String, nullable=False, unique=False)


class URLSheet(Base):
    """Без вопросов, я не готов"""
    url = Column(String)


class Maintenance(Base):
    """Я до конца уклонялся от этой хрени"""
    datatime = Column(DateTime, default=moscow_now(MOSCOW_TZ))
    last_updata_men = Column(String, nullable=False)
    last_updata_men_sur = Column(String, nullable=False)
    whot_swap = Column(String, nullable=False)
    wire_mark = Column(String, nullable=True, default='-')
    wire_diameter = Column(Float, nullable=True, default=0)
    name_gaz = Column(String, nullable=True, default='-')
    robot_id = Column(Integer, nullable=True)

