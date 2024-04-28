from sqlalchemy import Column, String, Text, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models.model_mixins import BaseInvestModel


class CharityProject(Base, BaseInvestModel):
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)

    @staticmethod
    async def get_open_projects(obj, session: AsyncSession) -> list[
            'CharityProject']:
        open_projects = await session.execute(
            select(obj).where(obj.fully_invested == 0).order_by(
                obj.create_date))
        return open_projects.scalars().all()
