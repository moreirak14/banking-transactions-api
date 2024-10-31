from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        populate_by_name = True
