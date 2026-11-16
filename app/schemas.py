# ----- Importing required modules and for created the alert schema ----- #
from datetime import datetime
from pydantic import Field, BaseModel

# ----- Creating a class inheririting the basemodel class for data validation ----- #
class AlertCreate(BaseModel):
    event_id: str = Field(min_length = 1, max_length = 100)
    source: str = Field(min_length = 1, max_length = 100)
    message: str = Field(min_length = 1, max_length = 100)
    timestamp: datetime