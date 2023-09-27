# to type hint @classmethod s
from __future__ import annotations


from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func
from sqlalchemy import select

from database.setup import Base
from schemas.click_details import ClickDetailsCreate


class ClickDetails(Base):
    __tablename__ = 'clickDetails'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, default="")

    clicks = relationship('Click',
                          backref='click_details',
                          lazy=True)

    @classmethod
    async def get_by_id(cls, db: Session, id: int) -> ClickDetails | None:
        q = select(cls).where(ClickDetails.id == id)
        result = await db.execute(q)
        result = result.fetchone()
        if result is not None:
            result = result[0]

        return result

    @classmethod
    async def get_page(cls, db: Session,
                       page_number: int = 1,
                       number_of_rows_per_page: int = 20
                       ) -> list[ClickDetails]:
        q = select(cls).limit(number_of_rows_per_page).\
                              offset(page_number * number_of_rows_per_page)
        result = await db.execute(q)
        result = result.fetchall()  # list like [(Model(...)), (Model(...))]
        result = [i[0] for i in result]  # convert to [Model(...), Model(...)]

        return result

    @classmethod
    async def create(cls, db: Session,
                     click_details: ClickDetailsCreate) -> ClickDetails:
        instance = cls(
            name=click_details.name,
            description=click_details.description
        )
        db.add(instance)
        await db.commit()

        return instance


class Click(Base):
    __tablename__ = 'clicks'

    id = Column(Integer, primary_key=True)
    details = Column(Integer, ForeignKey('clickDetails.id'))
    last_click = Column(Integer)
    time = Column(DateTime, default=func.now())

    # click_details = relationship('ClickDetails', backref='clicks')
