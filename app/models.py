#Import Base Class from database.py to inherit Declarative Class attributes
from app.database import Base

#Import datetime class to assign timestamp data type
from datetime import datetime

#Import sqlalchemy object Relational Mapper class to get objects like Mapped and mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

class Alerts(Base):
    __tablename__ = "System_Alerts"

    alert_id: Mapped[int] = mapped_column(primary_key = True)
    event_id: Mapped[str] = mapped_column(String(100), nullable = False)
    source: Mapped[str] = mapped_column(String(100), nullable = False)
    owner_email: Mapped[str] = mapped_column(String(350), nullable = False)
    message: Mapped[str] = mapped_column(String(100), nullable = False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone = True), nullable = False)