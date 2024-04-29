from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def close_charity_projects(obj: CharityProject) -> CharityProject:
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.utcnow()
    return obj


async def funds_distribution(obj: Union[CharityProject, Donation],
                             project: Union[CharityProject, Donation]
                             ) -> tuple[
        Union[CharityProject, Donation], Union[CharityProject, Donation]]:
    remaining_amount = obj.full_amount - obj.invested_amount
    remaining_project_amount = project.full_amount - project.invested_amount

    if remaining_amount >= remaining_project_amount:
        obj.invested_amount += remaining_project_amount
    else:
        project.invested_amount += remaining_amount

    await close_charity_projects(obj)
    if remaining_amount >= remaining_project_amount:
        await close_charity_projects(project)

    return obj, project


async def invest(obj, model, session: AsyncSession) -> Union[
        CharityProject, Donation]:
    available_projects = await CharityProject.get_open_projects(model, session)
    if available_projects:
        for project in available_projects:
            obj, model = await funds_distribution(obj, project)
            session.add(obj)
            session.add(project)
        await session.commit()
        await session.refresh(obj)
    return obj
