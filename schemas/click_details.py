from pydantic import BaseModel


class ClickDetailsGET(BaseModel):
    id: int
    name: str
    description: str | None = ""


class ClickDetailsCreate(BaseModel):
    name: str
    description: str | None = ""
