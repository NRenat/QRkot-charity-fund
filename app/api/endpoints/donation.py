from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User, CharityProject, Donation
from app.schemas.donation import DonationDBSuperUser, DonationDB, \
    DonationCreate
from app.services.invest import invest

router = APIRouter()


@router.get('/', response_model=list[DonationDBSuperUser],
            dependencies=[Depends(current_superuser)])
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)) -> list[Donation]:
    donations = await donation_crud.get_multi(session)
    return donations


@router.post('/', response_model=DonationDB, response_model_exclude_none=True)
async def create_new_donation(donation: DonationCreate,
                              session: AsyncSession = Depends(
                                  get_async_session),
                              user: User = Depends(current_user)) -> Donation:
    new_donation = await donation_crud.create(donation, session, user)
    new_donation = await invest(new_donation, CharityProject, session)
    return new_donation


@router.get('/my', response_model=list[DonationDB])
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)) -> list[Donation]:

    donations = await donation_crud.get_donations_for_user(session, user)
    return donations
