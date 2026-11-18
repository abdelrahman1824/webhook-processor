# Webhook Processor

## Run

```bash
git clone https://github.com/abdelrahman1824/webhook-processor.git
cd webhook-processor
docker compose build
docker compose up
```

Check the container:

```bash
docker compose ps
```

Open Swagger UI:

```text
http://localhost:8000/docs
```

## Test `POST /webhook`

In Swagger UI:

1. Expand `POST /webhook`.
2. Click **Try it out**.
3. Submit one of the following payloads.
4. Feel free to add any email so you can test the Email alert
5. Click **Execute**.

### Valid Alert

Expected: `200 OK`

```json
{
  "event_id": "evt_0001",
  "source": "server_1",
  "owner_email": "owner@example.com",
  "message": "High CPU usage",
  "timestamp": "2026-11-18T15:37:46Z"
}
```

### Invalid Email

Expected: `422 Unprocessable Content`

```json
{
  "event_id": "evt_0002",
  "source": "server_1",
  "owner_email": "invalid-email",
  "message": "High CPU usage",
  "timestamp": "2026-11-18T15:37:46Z"
}
```

### Invalid Timestamp

Expected: `422 Unprocessable Content`

```json
{
  "event_id": "evt_0003",
  "source": "server_1",
  "owner_email": "owner@example.com",
  "message": "High CPU usage",
  "timestamp": "invalid-timestamp"
}
```

### Missing Required Field

Expected: `422 Unprocessable Entity`

```json
{
  "event_id": "evt_0004",
  "source": "server_1",
  "owner_email": "owner@example.com",
  "timestamp": "2026-11-18T15:37:46Z"
}
```

## View Stored Alerts

Use `GET /alerts` in Swagger UI or open:

```text
http://localhost:8000/alerts
```

## Stop

If you have the logs displaying in the terminal just press d to dettach

```bash
docker compose down
```

## Reset the Alerts Database

```bash
docker compose down -v
docker compose up --build -d
```

> Gmail credentials are excluded from the repository. Alert storage and retrieval remain available if email notification fails.