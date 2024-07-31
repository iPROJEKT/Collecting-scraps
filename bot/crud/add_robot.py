from bot.models.base import AsyncSessionLocal
from bot.models.models import RobotState


async def create_robot() -> RobotState:
    result = RobotState(
        id_robot=2,
        wire=8,
        wire_mark='СВ08Г2С-О',
        wire_diameter=1.0,
        busy=False
    )
    async with AsyncSessionLocal() as session:
        session.add(result)
        await session.commit()
        await session.refresh(result)
    return result
