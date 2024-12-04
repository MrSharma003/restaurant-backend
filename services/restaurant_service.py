from bson import ObjectId
from models.restaurant import Restaurant
from db import Database

class RestaurantService:
    def __init__(self):
        self.collection = Database.get_instance()["restaurant_db"]["restaurants"]

    def register_restaurant(self, restaurant: Restaurant):
        return str(self.collection.insert_one(restaurant.__dict__).inserted_id)

    def search_restaurant(self, filters: dict):
        results = self.collection.find(filters)
        return [
            {
                **restaurant,
                "_id": str(restaurant["_id"])
            }
            for restaurant in results
        ]
