# ----- Importing required dependencies to create the endpoints ----- #
from fastapi import FastAPI, status, Depends
from app.schemas import AlertCreate
from app.database import engine, Base, get_db
from app.models import Alerts
from sqlalchemy import select
from sqlalchemy.orm import Session
import time 

#API app
app = FastAPI(title = "Webhook Processor",
              description = "Recieves, processes and stores External Systems alerts",
              version = "1.0.0")

Base.metadata.create_all(bind = engine)

#API POST request endpoint webhook
@app.post("/webhook", status_code = status.HTTP_201_CREATED)
def recieve_webhook(alert: AlertCreate, db: Session = Depends(get_db)):
    time.sleep(3)

    new_alert = Alerts(event_id = alert.event_id,
                       source = alert.source,
                       message = alert.message,
                       timestamp = alert.timestamp)

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    
    return f"Event with the id {new_alert.event_id} has been stored in the database with an ID of {new_alert.alert_id}"

@app.get("/alerts")
def show_alerts(db: Session = Depends(get_db)):
    alerts = db.scalars(select(Alerts)).all()

    if not alerts:
        return "No alerts stored!"

    return [{
        "alert_id": alert.alert_id,
        "event_id": alert.event_id,
        "source": alert.source,
        "message": alert.message,
        "timestamp": alert.timestamp
    } for alert in alerts]