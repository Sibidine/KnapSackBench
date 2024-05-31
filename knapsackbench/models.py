from pydantic import BaseModel

class Constraints(BaseModel):
    weights: list
    values: list
    limit: int
    items: int
