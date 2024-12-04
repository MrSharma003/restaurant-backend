from pydantic import BaseModel

class RestaurantSchema(BaseModel):
    # id: str  # Use 'id' instead of '_id' for cleaner responses
    name: str
    city: str
    area: str
    cuisine: str
    rating: float
    cost_for_two: float
    is_veg: bool

    class Config:
        orm_mode = True