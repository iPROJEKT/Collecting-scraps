from datetime import timedelta

from sqlalchemy import select

from bot.core.utils import moscow_now
from bot.models.base import AsyncSessionLocal
from bot.models.models import LilWAAMerNigga, RobotState, MOSCOW_TZ, Incident, Observations


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


async def add_updata_for_robot(
    robot: int,
    diametr: float,
    mark: str,
    last_updata_men: str,
    last_updata_men_sur: str
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
        robot.last_updata_men = last_updata_men
        robot.tip_data_change = moscow_now(MOSCOW_TZ)
        robot.wire = 10
        robot.last_updata_men_sur = last_updata_men_sur
        await session.commit()
        await session.refresh(robot)


async def add_updata_tip(
    robot_id: int,
    last_updata_men: str,
    last_updata_men_sur: str
) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(RobotState).where(
                RobotState.id_robot == robot_id
            )
        )
        robot = result.scalar_one_or_none()
        robot.last_updata_men = last_updata_men
        robot.last_updata_men_sur = last_updata_men_sur
        robot.tip_data_change = moscow_now(MOSCOW_TZ)
        await session.commit()
        await session.refresh(robot)


async def add_updata_gaz(
    robot: int,
    last_updata_men: str,
    gaz_name: str,
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
        robot.name_gaz = gaz_name
        robot.gaz_state = 10.0
        robot.tip_data_change = moscow_now(MOSCOW_TZ)
        await session.commit()
        await session.refresh(robot)


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
) -> None:
    istens = await get_current_robot_statistic(robot)
    async with AsyncSessionLocal() as session:
        result = Incident(
            number_robot=robot,
            incident=name_of_defect,
            comment=what_happened,
            name_main_programm=name_mp,
            coord=defect_coordinates,
            name_user=f'{istens.last_updata_men} {istens.last_updata_men_sur}'
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


async def get_all_incident() -> Incident:
    ten_minutes_ago = moscow_now(MOSCOW_TZ) - timedelta(minutes=10)
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Incident)
        )
        return result.scalars().all()
