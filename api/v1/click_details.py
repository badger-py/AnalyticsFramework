from fastapi import APIRouter, Depends, HTTPException, Query

from schemas.click_details import ClickDetailsGET, ClickDetailsCreate
from services.click_details import ClickDetailsService
from database.deps import get_db


router = APIRouter(tags=["Click Details Endpoints"])


@router.get("/")
async def get_click_details(id: int,
                            db=Depends(get_db)) -> ClickDetailsGET | None:
    click_details = await ClickDetailsService.get_by_id(db=db, id=id)

    if click_details is None:
        raise HTTPException(
            404, detail="Not found"
        )
    return click_details

@router.get("/pagination", description="Returns all ClickDetail objects in the specified range.")
async def get_pagination_click_details(page_number: int = Query(ge=0, description="Can only be 0 (first element) or bigger"),
                                       number_of_rows_per_page: int = Query(ge=1, description="Can only be 1 or above"),
                                       db=Depends(get_db)) -> list[ClickDetailsGET]:
    return await ClickDetailsService.get_all(db=db, page_number=page_number,
                                       number_of_rows_per_page=number_of_rows_per_page)


@router.put("/")
async def create_click_details(new_click_details: ClickDetailsCreate,
                               db=Depends(get_db)) -> ClickDetailsGET:
    return await ClickDetailsService.create(db, new_click_details)
