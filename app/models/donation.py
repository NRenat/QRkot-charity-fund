from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.model_mixins import BaseInvestModel


class Donation(Base, BaseInvestModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
