from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from schema.restaurantSchema import RestaurantSchema
from schema.slotSchema import SlotSchema
from services.restaurant_service import RestaurantService
from services.slot_service import SlotService

class TableBookingRequest(BaseModel):
    slot_id: str
    table_id: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

restaurant_service = RestaurantService()
slot_service = SlotService()

@app.post("/register")
def register_restaurant(restaurant: RestaurantSchema):
    restaurant_id = restaurant_service.register_restaurant(restaurant)
    return {"restaurant_id": str(restaurant_id)}

@app.post("/slots")
def add_slot(slot: SlotSchema):
    slot_id = slot_service.add_slot(slot)
    return {"slot_id": str(slot_id)}

@app.get("/restaurants/search")
def search_restaurant(name: str = None, city: str = None, area: str = None, cuisine: str = None):
    filters = {key: value for key, value in locals().items() if value is not None}
    results = restaurant_service.search_restaurant(filters)
    
    restaurants = [
        {
            "id": restaurant["_id"],
            **{key: value for key, value in restaurant.items() if key != "_id"}
        }
        for restaurant in results
    ]
    
    return {"restaurants": restaurants}


@app.get("/slots/available/{restaurant_id}")
def get_available_slots(restaurant_id: str):
    slots = slot_service.get_available_slots(restaurant_id)
    return {"available_slots": slots}

@app.post("/tables/book")
def book_table(booking_request: TableBookingRequest):
    success = slot_service.book_table(booking_request.slot_id, booking_request.table_id)
    if not success:
        raise HTTPException(status_code=400, detail="Table is either already booked or slot does not exist.")
    return {"message": "Table booked successfully"}