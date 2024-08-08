from typing import List

from sqlalchemy import desc, func
from sqlalchemy import select

from bot.core.utils import moscow_now
from bot.models.base import AsyncSessionLocal
from bot.models.models import LilWAAMerNigga, RobotState, MOSCOW_TZ, Incident, Observations, URLSheet, Maintenance


async def create_user(
    telegramm_id: int,
    name: str,
    surname: str
) -> LilWAAMerNigga:
    result = LilWAAMerNigga(
        user_id=telegramm_id,
        name=name,
        surname=surname
    )
    async with AsyncSessionLocal() as session:
        session.add(result)
        await session.commit()
        await session.refresh(result)
    return result


async def get_user_by_id(
    telegramm_id: int,
):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(LilWAAMerNigga).where(
                LilWAAMerNigga.user_id == telegramm_id
            )
        )
        user = result.scalar_one_or_none()
    return user


async def add_robot_for_operator(
    robot: int,
    telegramm_id: int,
) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(LilWAAMerNigga).where(
                LilWAAMerNigga.user_id == telegramm_id
            )
        )
        user = result.scalar_one_or_none()
        user.robot_id = robot
        await session.commit()
        await session.refresh(user)


async def get_cell_number(
    telegramm_id: int
) -> LilWAAMerNigga:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(LilWAAMerNigga.robot_id).where(
                LilWAAMerNigga.user_id == telegramm_id
            )
        )
        return result.scalars().first()


async def get_current_robot_statistic(
    robot_id: int
) -> RobotState:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(RobotState).where(
                RobotState.id_robot == robot_id
            )
        )
        return result.scalars().first()


async def create_maintenance_record(
    whot_swap=None,
    wire_mark='-',
    wire_diameter: float = 0.0,
    last_updata_men=None,
    last_updata_men_sur=None,
    robot_id=None,
    name_gaz='-',
    session=None
) -> None:
    maintenance_record = Maintenance(
        whot_swap=whot_swap,
        wire_mark=wire_mark,
        wire_diameter=wire_diameter,
        last_updata_men=last_updata_men,
        last_updata_men_sur=last_updata_men_sur,
        robot_id=robot_id,
        name_gaz=name_gaz,
    )
    session.add(maintenance_record)
    await session.commit()
    await session.refresh(maintenance_record)


async def add_updata_for_robot(
    robot: int,
    diametr: float,
    mark: str,
    last_men: str,
    last_men_sur: str
) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(RobotState).where(
                RobotState.id_robot == robot
            )
        )
        robot = result.scalar_one_or_none()
        robot.wire_mark = mark
        robot.wire_diameter = diametr
        robot.last_updata_men = last_men
        robot.tip_data_change = moscow_now(MOSCOW_TZ)
        robot.wire = 10
        robot.last_updata_men_sur = last_men_sur
        await session.commit()
        await session.refresh(robot)
        await create_maintenance_record(
            session=session,
            robot_id=robot.id_robot,
            wire_mark=mark,
            last_updata_men=last_men,
            last_updata_men_sur=last_men_sur,
            whot_swap='Замента проволки',
            wire_diameter=diametr
        )


async def add_updata_tip(
    robot_id: int,
    last_men: str,
    last_men_sur: str
) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(RobotState).where(
                RobotState.id_robot == robot_id
            )
        )
        robot = result.scalar_one_or_none()
        robot.last_updata_men = last_men
        robot.last_updata_men_sur = last_men_sur
        robot.tip_data_change = moscow_now(MOSCOW_TZ)
        await session.commit()
        await session.refresh(robot)
        await create_maintenance_record(
            session=session,
            whot_swap='Замена наконечника',
            last_updata_men=last_men,
            last_updata_men_sur=last_men_sur,
            robot_id=robot.id_robot
        )


async def add_updata_gaz(
    robot: int,
    last_men: str,
    gaz_name: str,
    last_men_sur: str
) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(RobotState).where(
                RobotState.id_robot == robot
            )
        )
        robot = result.scalar_one_or_none()
        robot.last_updata_men = last_men
        robot.last_updata_men_sur = last_men_sur
        robot.name_gaz = gaz_name
        robot.gaz_state = 10.0
        robot.tip_data_change = moscow_now(MOSCOW_TZ)
        await session.commit()
        await session.refresh(robot)
        await create_maintenance_record(
            session=session,
            whot_swap='Замена газа',
            name_gaz=gaz_name,
            last_updata_men=last_men,
            last_updata_men_sur=last_men_sur,
            robot_id=robot.id_robot
        )


async def updata_gaz_ware(
    robot: int,
    last_updata_men: str,
    gaz_count: float,
    ware_count: int,
    last_updata_men_sur: str
) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(RobotState).where(
                RobotState.id_robot == robot
            )
        )
        robot = result.scalar_one_or_none()
        robot.last_updata_men = last_updata_men
        robot.last_updata_men_sur = last_updata_men_sur
        robot.wire = ware_count
        robot.gaz_state = gaz_count
        robot.tip_data_change = moscow_now(MOSCOW_TZ)
        await session.commit()
        await session.refresh(robot)


async def create_defect(
    robot: int,
    name_of_defect: str,
    what_happened: str,
    name_mp: str,
    defect_coordinates: str,
    name_user: LilWAAMerNigga,
) -> None:
    async with AsyncSessionLocal() as session:
        result = Incident(
            number_robot=robot,
            incident=name_of_defect,
            comment=what_happened,
            name_main_programm=name_mp,
            coord=defect_coordinates,
            name_user=f'{name_user.name} {name_user.surname}'
        )
        session.add(result)
        await session.commit()
        await session.refresh(result)


async def save_observations(
    user_id: int,
    id_robot: int,
    comment: str
) -> None:
    result = Observations(
        user_id=user_id,
        id_robot=id_robot,
        comment=comment
    )
    async with AsyncSessionLocal() as session:
        session.add(result)
        await session.commit()
        await session.refresh(result)


async def get_all_incident() -> List[Incident]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Incident).where(
                func.date(Incident.datatime) == moscow_now(MOSCOW_TZ).date()
            )
        )
        return result.scalars().all()


async def create_url(
    url: str
) -> None:
    result = URLSheet(
        url=url
    )
    async with AsyncSessionLocal() as session:
        session.add(result)
        await session.commit()
        await session.refresh(result)


async def ger_url() -> str:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(URLSheet.url).order_by(desc(URLSheet.id))
        )
        return result.scalars().first()


async def get_all_observations() -> List[Observations]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Observations)
        )
        return result.scalars().all()


async def get_all_maintenance() -> List[Maintenance]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Maintenance).where(
                func.date(Maintenance.datatime) == moscow_now(MOSCOW_TZ).date()
            )
        )
        return result.scalars().all()
