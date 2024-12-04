from datetime import datetime
from typing import List, Dict

class Slot:
    def __init__(self, restaurant_id: str, start_time: datetime, end_time: datetime, tables: List[Dict]):
        self.restaurant_id = restaurant_id
        self.start_time = start_time
        self.end_time = end_time
        self.tables = tables
