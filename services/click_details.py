from sqlalchemy.orm import Session

from schemas.click_details import ClickDetailsGET, ClickDetailsCreate
from database.models.click import ClickDetails


class ClickDetailsService():
    @staticmethod
    async def get_by_id(db: Session, id: int) -> ClickDetailsGET | None:
        return await ClickDetails.get_by_id(db=db, id=id)

    @staticmethod
    async def create(db: Session, click_details: ClickDetailsCreate) -> ClickDetailsGET:
        return await ClickDetails.create(db, click_details)

    @staticmethod
    async def get_all(
                db: Session,
                page_number: int,
                number_of_rows_per_page: int
            ) -> list[ClickDetailsGET]:
        result = await ClickDetails.get_page(db=db, page_number=page_number,
                                           number_of_rows_per_page=number_of_rows_per_page)
        # convert to pydantic format. from_attributes=True makes it work with ORM
        return [ClickDetailsGET.model_validate(i, from_attributes=True) for i in result]
