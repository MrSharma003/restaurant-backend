from fastapi import HTTPException
from db import Database
from models.slot import Slot
from bson import ObjectId


class SlotService:
    def __init__(self):
        self.collection = Database.get_instance()["restaurant_db"]["slots"]

    def add_slot(self, slot: Slot):
        return self.collection.insert_one(slot.__dict__).inserted_id

    def get_available_slots(self, restaurant_id: str):
        slots = self.collection.find({"restaurant_id": restaurant_id})
        available_slots = []

        for slot in slots:
            # Convert ObjectId to string
            slot["_id"] = str(slot["_id"])
            slot["available_tables"] = [table for table in slot["tables"] if table["is_available"]]
            available_slots.append(slot)

        return available_slots

    def book_table(self, slot_id: str, table_id: str):
        slot = self.collection.find_one(
            {"_id": ObjectId(slot_id), "tables.table_id": table_id}
        )

        if not slot:
            raise HTTPException(status_code=404, detail="Slot not found")

        # Check if the table is available
        table = next((t for t in slot["tables"] if t["table_id"] == table_id), None)
        if not table or not table["is_available"]:
            raise HTTPException(status_code=400, detail="Table is already booked")

        # Proceed to update the table availability to false atomically
        result = self.collection.update_one(
            {"_id": ObjectId(slot_id), "tables.table_id": table_id, "tables.is_available": True},
            {"$set": {"tables.$.is_available": False}}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Failed to book table or already booked")

        return {"message": "Table booked successfully"}