from typing import Optional

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(self.model.id).where(
                self.model.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[str]:
        projects = await session.execute(
            select(
                [
                    self.model.name,
                    (
                        func.julianday(self.model.close_date) -
                        func.julianday(self.model.create_date)
                    ).label('duration'),
                    self.model.description
                ]
            ).where(self.model.fully_invested).order_by(desc('duration')))

        return projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
