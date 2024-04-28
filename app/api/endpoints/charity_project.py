from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_name_duplicate, check_project_exists,
                                check_project_already_invested,
                                check_closed_project,
                                check_set_invested_amount)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation, CharityProject
from app.schemas.charity_project import (CharityProjectDB,
                                         CharityProjectCreate,
                                         CharityProjectUpdate)
from app.utils.utils import invest

router = APIRouter()


@router.post('/', response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)])
async def create_new_charity_project(charity_project: CharityProjectCreate,
                                     session: AsyncSession = Depends(
                                         get_async_session)) -> CharityProject:
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project,
                                                    session)
    new_charity_project = await invest(new_project, Donation, session)
    return new_charity_project


@router.get("/", response_model=list[CharityProjectDB],
            response_model_exclude_none=True)
async def get_all_charity_projects(
        session: AsyncSession =
        Depends(get_async_session)) -> list[CharityProject]:
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.delete('/{project_id}', response_model=CharityProjectDB,
               dependencies=[Depends(current_superuser)])
async def remove_project(project_id: int, session: AsyncSession = Depends(
        get_async_session)) -> CharityProject:
    project = await check_project_exists(project_id, session)
    project = await charity_project_crud.remove(project,
                                                session)
    await check_project_already_invested(project)

    return project


@router.patch('/{project_id}', response_model=CharityProjectDB,
              dependencies=[Depends(current_superuser)])
async def partially_update_charity_project(
        project_id: int,
        obj: CharityProjectUpdate,
        session: AsyncSession = Depends(
            get_async_session)) -> CharityProject:
    project = await check_project_exists(project_id, session)
    if obj.name:
        await check_name_duplicate(obj.name, session)

    await check_closed_project(project)
    if obj.full_amount:
        await check_set_invested_amount(project, obj.full_amount)

    project = await charity_project_crud.update(project, obj, session)
    return project
