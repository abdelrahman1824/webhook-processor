# ----- Importing required dependencies to create the endpoints ----- #
from fastapi import FastAPI, status, Depends

from app.schemas import AlertCreate
from app.database import engine, Base, get_db
from app.models import Alerts
from sqlalchemy import select
from sqlalchemy.orm import Session

import time 

from app.services.send_gmail import send_email

#API app
app = FastAPI(title = "Webhook Processor",
              description = "Recieves, processes and stores External Systems alerts",
              version = "1.0.0")

Base.metadata.create_all(bind = engine)

@app.get("/")
def home_page_description():
    return """This is the Webhook-Alert Application 
    Extend the url to /alerts to see all stored alerts
    Extend the url to /webhook to test alert requests"""

#API POST request endpoint webhook
@app.post("/webhook")
def recieve_webhook(alert: AlertCreate, db: Session = Depends(get_db)):
    time.sleep(3)

    new_alert = Alerts(event_id = alert.event_id,
                       source = alert.source,
                       owner_email = alert.owner_email,
                       message = alert.message,
                       timestamp = alert.timestamp)

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    #Send email with alert to the source owner
    try:
        gmail_message_id = send_email(
            event_id = new_alert.event_id,
            source = new_alert.source,
            owner_email = new_alert.owner_email,
            message = new_alert.message,
            timestamp = new_alert.timestamp
        )

        email_status = "Sent"

    except Exception as e:
        print(f"Email notification error, details: {e}")

        gmail_message_id = None
        email_status = "Failed"
    
    return {
        "status": "processed",
        "message": "Alert processed and stored successfully",
        "alert": {
            "alert_id": new_alert.alert_id,
            "event_id": new_alert.event_id,
            "source": new_alert.source,
            "owner_email": new_alert.owner_email,
            "message": new_alert.message,
            "timestamp": new_alert.timestamp,
        },
        "notification": {
            "email_status": email_status,
            "gmail_message_id": gmail_message_id,
        },
    }

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