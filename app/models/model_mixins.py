from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime


class BaseInvestModel:
    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    close_date = Column(DateTime)
