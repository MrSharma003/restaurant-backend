from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

class SlotSchema(BaseModel):
    restaurant_id: str
    start_time: datetime
    end_time: datetime
    tables: List[Dict] 